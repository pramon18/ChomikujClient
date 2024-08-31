using Models;
using SQLite;

namespace Database
{
    public class DB
    {
        private static SQLiteAsyncConnection? _connection = null;
        private static readonly string _databasePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "chomik.db3");

        public static SQLiteAsyncConnection Connection 
        { 
            get 
            {
                if (_connection == null)
                    _connection = new SQLiteAsyncConnection(_databasePath, true);

                System.Diagnostics.Debug.WriteLine(_databasePath);

                return _connection;
            } 
        }

        public async static void CreateTables()
        {
            await Connection.CreateTableAsync<Folder>();
            await Connection.CreateTableAsync<Models.File>();
        }
    }
}
