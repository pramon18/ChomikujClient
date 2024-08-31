using System.Security.Cryptography;
using System.Text;

namespace Util
{
    public static class HashUtil
    {
        public static String ComputeMD5(String value)
        {
            var result = String.Empty;

            using (var md5 = MD5.Create())
            {
                var bytes = md5.ComputeHash(Encoding.UTF8.GetBytes(value));
                result = BitConverter.ToString(bytes, 0, bytes.Length).Replace("-", "").ToLower();
            }
            return result;
        }
    }
}
