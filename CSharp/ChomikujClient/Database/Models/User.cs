using SQLite;

namespace Models
{
    public class User
    {
        [PrimaryKey]
        public Int64 ID { get; set; }
        public string Name { get; set; }
        public string? Token { get; set; }
    }
}
