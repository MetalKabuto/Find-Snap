using Microsoft.Maui.Controls.PlatformConfiguration.WindowsSpecific;
using static FrontendMAUIApplication.MainPage;
using RestSharp;
using System.Text.Json;
using Microsoft.Maui.Graphics.Platform;
using System.Runtime.CompilerServices;
using IImage = Microsoft.Maui.Graphics.IImage;
using System.Globalization;

namespace FrontendMAUIApplication
{
    public partial class MainPage : ContentPage
    {
        public static MainPage mainPage = new();

        public MainPage()
        {
            InitializeComponent();
            mainPage = this;
        }

        private void StartBtn_Clicked(object sender, EventArgs e)
        {
            GameHandler.StartGame();
        }

        private void CameraBtn_Clicked(object sender, EventArgs e)
        {
            MediaHandler.TakePhoto();
        }

        private void SubmitBtn_Clicked(object sender, EventArgs e)
        {
            double resultPercent = GameHandler.ComparePhoto();
            //The lowest possible percent is 0. It exists to check that the page doesn't switch if the user submits and empty image.
            if (resultPercent != -1)
            {
                //Switches to a second window to display the results in.
                Navigation.PushAsync(new ResultPage(resultPercent));
            }
            else
            {
                //do nothing
            }
        }
    }

    public partial class ResultPage : ContentPage
    {
        public double percent;

        //When you make a new resultpage object, initialize creates a new window and the text on the new page changes as well.
        public ResultPage(double matchPercent)
        {
            InitializeComponent();
            percent = matchPercent;
            string percentString = percent.ToString();
            ratioText.Text = $"{percentString}% match ratio!";
            if (percent >= 50)
            {
                resultText.Text = "Your photo matches the category!";
            }
            else
            {
                resultText.Text = "Your photo doesn't match the category...";
            }
        }
    }

    public static class GameHandler
    {
        static int CategoryInt = 0;
        static string[] categories = JsonSerializer.Deserialize<string[]>(
            ClientService.Get<string>().Content
            );
        static string Category() => categories[CategoryInt];
        static ImageSource CategoryImage() => ClientService.GetImage(Category());
        
        public static void StartGame()
        {

            Random rand = new();
            CategoryInt = rand.Next(0, categories.Length);

            mainPage.CategoryImage.Source = CategoryImage();
            mainPage.CategoryName.Text = Category();
            mainPage.CategoryText.Text = $"Take a photo of a {Category()} to finish this assignment";
            mainPage.CategoryImage.IsVisible = true;
            mainPage.CameraBtn.IsEnabled = true;
            mainPage.CameraBtn.IsVisible = true;
            mainPage.SubmitBtn.IsEnabled = true;
            mainPage.SubmitBtn.IsVisible = true;

            mainPage.StartBtn.IsEnabled = false;
            mainPage.StartBtn.IsVisible = false;

        }

        public static double ComparePhoto()
        {
            RestResponse response = ClientService.Post(MediaHandler.image);
            //Made it so that the program doesn't crash if you user sends in an empty image.
            if (response == null)
            {
                mainPage.CategoryText.Text = "You need to take a picture before sending it!";
                return 0;
            }
            //If the user sends a picture, it works like before.
            else
            {
                Dictionary<string, string> predictCategories = JsonSerializer.Deserialize<Dictionary<string, string>>(response.Content);
                string result = predictCategories[Category()];
                result = result.Remove(result.Length - 1);

                int percent = (int) Math.Round(double.Parse(result.Replace(',', '.'), CultureInfo.InvariantCulture));

                // TODO: Result screen with points
                if (percent >= 50)
                {
                    //mainPage.CategoryName.Text = $"You win! Your photo has the following ratio: {percent}%";
                    mainPage.CategoryText.Text = $"Select Start Game to get another assignment";
                    mainPage.CameraBtn.IsVisible = false;
                    mainPage.SubmitBtn.IsVisible = false;
                }
                else
                {
                    //mainPage.CategoryName.Text = $"Sorry, no match. Your photo has the following ratio: {percent}%";
                    mainPage.CategoryText.Text = $"Submit another photo,\nor Start Game to get a new assignment";
                    mainPage.CameraBtn.IsVisible = true;
                    mainPage.SubmitBtn.IsVisible = true;
                }
                //Make the startbutton visible again
                mainPage.StartBtn.IsVisible = true;
                mainPage.StartBtn.IsEnabled = true;
                return percent;
            }
        }
    }

    public static class MediaHandler
    {
        public static MemoryStream image;
        public static string localFilePath = "";
        public static async void TakePhoto()
        {
            if (MediaPicker.Default.IsCaptureSupported)
            {
                FileResult photo = null;
                photo = await MediaPicker.Default.CapturePhotoAsync();
                if (photo != null)
                {
                    // save the file into local storage
                    localFilePath = Path.Combine(FileSystem.CacheDirectory, photo.FileName);


                    using Stream sourceStream = await photo.OpenReadAsync();
                    using FileStream localFileStream = File.OpenWrite(localFilePath);

                    await sourceStream.CopyToAsync(localFileStream);
                    mainPage.UserImage.Source = localFilePath;
                    mainPage.UserImage.IsVisible = true;
                    DownsizePhoto(photo, 400);
                }
                else
                    localFilePath = "";
            }
            else
                localFilePath = "";
        }
        public static async void DownsizePhoto(FileResult photo, float maxSize)
        {
            if (photo == null) return;

            using (Stream sourceStream = await photo.OpenReadAsync())
            {
                IImage image = PlatformImage.FromStream(sourceStream);
                using (IImage downsizedImage = image.Downsize(maxSize, true)) //disposes of 'image'
                {
                    // Save the resized image to stream attribute
                    MediaHandler.image = new MemoryStream();
                    await downsizedImage.SaveAsync(MediaHandler.image, ImageFormat.Jpeg);
                    MediaHandler.image.Position = 0;
                }
            }

        }
        
    }

}
