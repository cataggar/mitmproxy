
// dotnet tool install -g dotnet-script
// dotnet script gcs4.csx

using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Security.Cryptography.X509Certificates;

var certPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "certs", "gcs.ppe.monitoring.core.windows.net.pem");
var certPem = File.ReadAllText(certPath);
var cert = X509Certificate2.CreateFromPem(certPem, certPem);

var url = "https://gcs.ppe.monitoring.core.windows.net/api/agent/v2/Test/SkyLink/MonitoringConfiguration/?Namespace=SkyLink&Version=Ver2v0.109&OSType=Linux";
var handler = new HttpClientHandler();
handler.ClientCertificates.Add(cert);

using (var client = new HttpClient(handler))
{
    var response = await client.GetAsync(url);
    Console.WriteLine($"status code: {response.StatusCode}");
    var json = await response.Content.ReadAsStringAsync();
    // Console.WriteLine(json);
    Console.WriteLine(JsonSerializer.Serialize(JsonSerializer.Deserialize<object>(json), new JsonSerializerOptions { WriteIndented = true }));
}
