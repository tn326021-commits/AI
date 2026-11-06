// File này dùng để giả lập các class của Unity khi biên dịch trên GitHub
// Nó KHÔNG ảnh hưởng đến game thật của bạn.
namespace UnityEngine
{
    public class Object { }
    public class Component : Object { public Transform transform { get; set; } }
    public class Behaviour : Component { }
    public class MonoBehaviour : Behaviour { }
    public class GameObject : Object
    {
        public Transform transform { get; set; }
        public T AddComponent<T>() where T : new() { return new T(); }
        public static GameObject FindWithTag(string tag) { return null; }
        public Component GetComponent(System.Type type) { return null; }
    }
    public class Transform : Component
    {
        public Vector3 position { get; set; }
        public Vector3 root { get; set; }
    }
    public class Camera : Behaviour
    {
        public static Camera main { get; set; }
        public Ray ScreenPointToRay(Vector3 pos) { return new Ray(); }
        public Transform transform { get; set; }
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
        public static Vector3 operator -(Vector3 a, Vector3 b) { return zero; }
    }
    public struct Quaternion
    {
        public static Quaternion LookRotation(Vector3 forward) { return new Quaternion(); }
        public static Quaternion Slerp(Quaternion a, Quaternion b, float t) { return new Quaternion(); }
        public static Vector3 operator *(Quaternion q, Vector3 v) { return v; }
    }
    public class Collider : Component { }
    public static class Physics
    {
        public static Collider[] OverlapSphere(Vector3 position, float radius) { return new Collider[0]; }
    }
    public static class Input
    {
        public static bool GetMouseButton(int button) { return false; }
    }
    public static class Time
    {
        public static float deltaTime => 0.016f;
    }
    public static class Screen
    {
        public static int width => 1920;
        public static int height => 1080;
    }
    public static class Debug
    {
        public static void Log(object message) { }
    }
}
