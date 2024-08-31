namespace ChomikujClient
{
    public partial class App : Application
    {
        public App()
        {
            InitializeComponent();

            AppDomain.CurrentDomain.UnhandledException += (s, e) =>
            {
                Exception ex = (Exception) e.ExceptionObject;
                System.Diagnostics.Debug.WriteLine(ex.Message);
                Console.WriteLine("Exceção inesperada...");
            };

            MainPage = new AppShell();
        }
    }
}
