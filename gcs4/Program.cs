
using System.Security.Cryptography.X509Certificates;
using System.Text.Json;

var certPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "certs", "gcs.ppe.monitoring.core.windows.net.pem");
var certPem = File.ReadAllText(certPath);
var cert = X509Certificate2.CreateFromPem(certPem, certPem);
if (Environment.OSVersion.Platform == PlatformID.Win32NT)
{
    cert = X509CertificateLoader.LoadPkcs12(cert.Export(X509ContentType.Pkcs12), null);
}

var url = "https://gcs.ppe.monitoring.core.windows.net/api/agent/v2/Test/SkyLink/MonitoringConfiguration/?Namespace=SkyLink&Version=Ver2v0.109&OSType=Linux";
var handler = new HttpClientHandler();
handler.ClientCertificates.Add(cert);

using (var client = new HttpClient(handler))
{
    var response = await client.GetAsync(url);
    Console.WriteLine($"status code: {response.StatusCode}");
    if (response.StatusCode == System.Net.HttpStatusCode.OK){
        var json = await response.Content.ReadAsStringAsync();
        // Console.WriteLine(json);
        Console.WriteLine(JsonSerializer.Serialize(JsonSerializer.Deserialize<object>(json), new JsonSerializerOptions { WriteIndented = true }));
    }
}
