using CommunityToolkit.Maui;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Services;
using Services.Interfaces;
using System.IO;
using System.Reflection;

namespace ChomikujClient
{
    public static class MauiProgram
    {
        public static IServiceProvider? Services { get; private set; }

        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder()
                                 .UseMauiApp<App>()
                                 .UseMauiCommunityToolkit()
                                 .ConfigureFonts(fonts =>
                                 {
                                     fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                                     fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
                                 });

            var assembly = Assembly.GetExecutingAssembly();
            using var stream = assembly.GetManifestResourceStream("ChomikujClient.appsettings.json");

            var config = new ConfigurationBuilder()
                    .AddJsonStream(stream)
                    .Build();

            builder.Configuration.AddConfiguration(config);

#if DEBUG
            builder.Logging.AddDebug();
#endif
            builder.Services.AddSingleton<IAPIService, APIService>();

            var app = builder.Build();

            Services = app.Services;

            return app;
        }        

        // Classes para configurações
        public class Settings
        {
            public NestedSettings User { get; set; } = null!;
        }

        public class NestedSettings
        {
            public string User { get; set; } = null!;
            public string Password { get; set; } = null!;
        }
    }
}
