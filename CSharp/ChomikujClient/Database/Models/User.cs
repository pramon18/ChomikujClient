using SQLite;

namespace Models
{
    public class User
    {
        [PrimaryKey]
        public string ChomikID { get; set; }
        public string Name { get; set; }
        public string? Token { get; set; }
    }
}
