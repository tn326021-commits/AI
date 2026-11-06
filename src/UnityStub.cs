using System;

namespace UnityEngine
{
    public class Object { public static void DontDestroyOnLoad(Object target) { } }
    public class Component : Object { public Transform transform { get; set; } public GameObject gameObject { get; set; } }
    public class Behaviour : Component { }
    public class MonoBehaviour : Behaviour { }
    
    public class GameObject : Object
    {
        public Transform transform { get; set; }
        public GameObject() { }
        public GameObject(string name) { }
        public T AddComponent<T>() where T : new() { return new T(); }
        public static GameObject FindWithTag(string tag) { return null; }
        public Component GetComponent(Type type) { return null; }
    }
    
    public class Transform : Component
    {
        public Vector3 position { get; set; }
        public Quaternion rotation { get; set; }
        public string name { get; set; }
        public Transform root { get; set; }
        public System.Collections.IEnumerator GetEnumerator() { return null; }
    }
    
    public class Camera : Behaviour
    {
        public static Camera main { get; set; }
        public Ray ScreenPointToRay(Vector3 pos) { return new Ray(); }
    }
    
    public class Ray { public Vector3 direction { get; set; } }
    
    public struct Vector3
    {
        public float x, y, z;
        public Vector3(float x, float y, float z) { this.x = x; this.y = y; this.z = z; }
        public static Vector3 up => new Vector3(0, 1, 0);
        public static Vector3 zero => new Vector3(0, 0, 0);
        public static Vector3 Cross(Vector3 a, Vector3 b) { return zero; }
        public float magnitude => 0;
        public Vector3 normalized => this;
        public static float Angle(Vector3 a, Vector3 b) { return 0; }
        public static Vector3 Lerp(Vector3 a, Vector3 b, float t) { return zero; }
        public static Vector3 operator -(Vector3 a, Vector3 b) { return zero; }
    }
    
    public struct Quaternion
    {
        public static Quaternion LookRotation(Vector3 forward) { return new Quaternion(); }
        public static Quaternion Slerp(Quaternion a, Quaternion b, float t) { return new Quaternion(); }
    }
    
    public class Collider : Component { }
    public struct RaycastHit { public Transform transform { get; set; } }

    public static class Physics
    {
        public static Collider[] OverlapSphere(Vector3 position, float radius) { return new Collider[0]; }
        public static bool Linecast(Vector3 start, Vector3 end, out RaycastHit hitInfo) { hitInfo = new RaycastHit(); return false; }
    }
    
    public static class Input
    {
        public static bool GetMouseButton(int button) { return false; }
        public static bool GetMouseButtonDown(int button) { return false; }
    }
    
    public static class Time { public static float time => 0; public static float deltaTime => 0.016f; }
    public static class Screen { public static int width => 1920; public static int height => 1080; }
    public static class Debug { public static void Log(object message) { } }

    // GIẢ LẬP ĐỒ HỌA NÂNG CAO
    public class Rect
    {
        public float x, y, width, height;
        public Rect(float x, float y, float width, float height) { this.x = x; this.y = y; this.width = width; this.height = height; }
    }

    public class Color
    {
        public float r, g, b, a;
        public Color(float r, float g, float b, float a) { this.r = r; this.g = g; this.b = b; this.a = a; }
        public static Color white => new Color(1,1,1,1);
        public static Color green => new Color(0,1,0,1);
    }

    public class Texture2D
    {
        public Texture2D(int w, int h) { }
        public void SetPixel(int x, int y, Color c) { }
        public void Apply() { }
    }

    public enum TextAnchor { MiddleCenter }
    public enum FontStyle { Bold }

    public class GUIStyle
{
    public GUIStyle() { }
    public GUIStyle(GUIStyle other) { } // Thêm hàm khởi tạo này
    public int fontSize { get; set; }
    public FontStyle fontStyle { get; set; }
    public TextAnchor alignment { get; set; }
    public GUIStyleState normal { get; set; } = new GUIStyleState();
    public GUIStyleState onNormal { get; set; } = new GUIStyleState();
    }

    public class GUIStyleState
    {
        public Color textColor { get; set; }
        public Texture2D background { get; set; }
    }

    public class GUISkin
    {
        public GUIStyle label { get; set; } = new GUIStyle();
        public GUIStyle button { get; set; } = new GUIStyle();
        public GUIStyle toggle { get; set; } = new GUIStyle();
        public GUIStyle box { get; set; } = new GUIStyle();
    }

    public static class GUI
    {
        public static GUISkin skin { get; set; } = new GUISkin();
        public static Rect Window(int id, Rect clientRect, Action<int> func, string text) { return clientRect; }
        public static void DragWindow(Rect r) { }
        public static void Box(Rect r, string text, GUIStyle style) { }
        public static void DrawTexture(Rect r, Texture2D t) { }
        public static void Label(Rect r, string text, GUIStyle style) { }
    }

    public static class GUILayout
    {
        public static void Space(float pixels) { }
        public static bool Toggle(bool value, string text, GUIStyle style) { return value; }
        public static void Label(string text, GUIStyle style) { }
        public static float HorizontalSlider(float value, float leftValue, float rightValue) { return value; }
        public static bool Button(string text, GUIStyle style) { return false; }
    }
}

namespace IFix { public class PatchAttribute : Attribute { } }
