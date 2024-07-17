using RestSharp;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace FrontendMAUIApplication
{
    /// <summary>
    /// ClientService contains a static RestClient to use in every API call. Use different requests to add endpoints and parameters (default = Method.Get) before making a call
    /// </summary>
    public class ClientService
    {
        private const string apiURL = "https://findnsnapapi-ojtg7u6dyq-lz.a.run.app";
        // static RestClient to use for every call. Ma
        private static readonly RestClient restClient = CreateClient(apiURL);

        private static RestClient CreateClient(string url = $"https://findnsnapapi-ojtg7u6dyq-lz.a.run.app")
        {
            var options = new RestClientOptions(url);
            var client = new RestClient(options);
            return client;
        }

        internal static RestResponse Post(string endpoint = "/predict", string image_path = "testimage.jpg")
        {
            try
            {
                var request = new RestRequest(endpoint, method: Method.Post);
                request.AddFile("image", image_path);
                var response = restClient.ExecutePost(request);
                string content = response.Content;
                Console.WriteLine(content);
                return response;
            }
            catch (System.ArgumentNullException)
            {
                return null;
            }
        }

        internal static RestResponse<T> Get<T>(string endpoint = "/categories")
        {
            var request = new RestRequest(endpoint, method: Method.Get);
            var response = restClient.Execute<T>(request);
            string content = response.Content;
            Console.WriteLine(content);
            return response;
            
        }

        internal static ImageSource GetImage(string category)
        {
            return ImageSource.FromUri(new Uri(apiURL + "/images/" + category));
        }
       
            //string content = await response.Content.ReadAsStringAsync();
            //return JsonSerializer.Deserialize<string[]>(content);           
     
    }
}
