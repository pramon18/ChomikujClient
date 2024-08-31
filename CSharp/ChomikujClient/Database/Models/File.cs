using SQLite;

namespace Models
{
    public class File
    {
        [PrimaryKey]
        public Int64 ID { get; set; }
        public String Name { get; set; }
    }
}
