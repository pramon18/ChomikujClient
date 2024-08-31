using System.Xml.Linq;

namespace Util
{
    public class XMLUtil
    {
        public static String GetValueByName(XDocument doc, String name)
        {
            var value = GetElementsByName(doc, name).FirstOrDefault()?.Value ?? String.Empty;
            return value;
        }

        public static IEnumerable<XElement> GetElementsByName(XDocument doc, String name)
        {
            var list = doc.Descendants().Where(x => x.Name.LocalName == name).ToList();
            return list;
        }

        public static String GetValueByName(XElement element, String name)
        {
            var value = GetElementsByName(element, name).FirstOrDefault()?.Value ?? String.Empty;
            return value;
        }

        public static IEnumerable<XElement> GetElementsByName(XElement element, String name)
        {
            var list = element.Descendants().Where(x => x.Name.LocalName == name).ToList();
            return list;
        }

        public static XElement? GetElementByName(XDocument doc, String name)
        {
            var element = GetElementsByName(doc, name).FirstOrDefault();
            return element;
        }
    }
}
