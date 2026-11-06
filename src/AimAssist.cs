using System;
using System.Reflection;
using UnityEngine;
using IFix;

namespace AimAssistMod
{
    public class AimAssistMenu : MonoBehaviour
    {
        // --- BIẾN CẤU HÌNH ---
        public static bool EnableAimLock = true;
        public static bool AimHeadNeck = false; // Chế độ bám Đầu + Cổ
        public static bool AntiBan = true;
        public static bool StealthMode = true;
        
        public static float HitboxSize = 1.2f; // Hitbox x3
        public static float AimSmooth = 25f;

        private bool _showMenu = false;
        private int _tapCount = 0;
        private float _lastTapTime = 0f;
        
        // Giao diện Menu
        private Rect _menuRect = new Rect(20, 20, 380, 420);
        private GUIStyle _titleStyle, _labelStyle, _toggleStyle, _buttonStyle, _boxStyle;
        private Texture2D _bgTexture, _titleTexture;

        private Camera _mainCam;
        private Transform _playerTransform;

        void Start()
        {
            _mainCam = Camera.main;
            _playerTransform = this.transform;
            InitStyles();
        }

        void Update()
        {
            // 1. NHẤP 4 LẦN ĐỂ MỞ MENU
            if (Input.GetMouseButtonDown(0))
            {
                if (Time.time - _lastTapTime > 0.5f) _tapCount = 0;
                _tapCount++;
                _lastTapTime = Time.time;
                if (_tapCount >= 4) { _showMenu = !_showMenu; _tapCount = 0; }
            }

            // 2. LOGIC AIM ASSIST
            if (!EnableAimLock || !Input.GetMouseButton(1)) return;
            if (_mainCam == null) _mainCam = Camera.main;
            if (_playerTransform == null) return;

            Ray ray = _mainCam.ScreenPointToRay(new Vector3(Screen.width / 2f, Screen.height / 2f, 0f));
            Vector3 aimDir = ray.direction;

            Collider[] targets = Physics.OverlapSphere(_playerTransform.position, 200f);
            Transform bestTarget = null;
            float bestScore = float.MaxValue;

            foreach (var col in targets)
            {
                if (col.transform.root == _playerTransform) continue;

                // Lấy điểm ngắm (Đầu hoặc Đầu+Cổ)
                Transform targetBone = AimHeadNeck ? GetHeadNeckTarget(col.gameObject) : GetHeadTarget(col.gameObject);
                if (targetBone == null) continue;

                Vector3 targetPos = targetBone.position;
                Vector3 toTarget = targetPos - _playerTransform.position;

                // Kiểm tra vật cản
                if (StealthMode)
                {
                    RaycastHit hit;
                    if (Physics.Linecast(_mainCam.transform.position, targetPos, out hit))
                    {
                        if (hit.transform.root != col.transform.root) continue; 
                    }
                }

                float distToRay = Vector3.Cross(aimDir, toTarget.normalized).magnitude * toTarget.magnitude;

                // Tính toán Hitbox (Nếu bật Hitbox)
                float currentHitbox = AimHeadNeck ? 0.5f : HitboxSize;

                if (distToRay <= currentHitbox)
                {
                    float angle = Vector3.Angle(aimDir, toTarget);
                    if (StealthMode && angle > 8f) continue; 

                    float score = distToRay + (toTarget.magnitude * 0.01f);
                    if (score < bestScore)
                    {
                        bestScore = score;
                        bestTarget = targetBone;
                    }
                }
            }

            if (bestTarget != null)
            {
                Vector3 targetDir = (bestTarget.position - _mainCam.transform.position).normalized;
                Quaternion targetRot = Quaternion.LookRotation(targetDir);
                _mainCam.transform.rotation = Quaternion.Slerp(_mainCam.transform.rotation, targetRot, Time.deltaTime * AimSmooth);
            }
        }

        // --- KHỞI TẠO GIAO DIỆN ĐẸP ---
        void InitStyles()
        {
            _bgTexture = new Texture2D(1, 1);
            _bgTexture.SetPixel(0, 0, new Color(0.1f, 0.1f, 0.1f, 0.95f)); // Nền đen mờ
            _bgTexture.Apply();

            _titleTexture = new Texture2D(1, 1);
            _titleTexture.SetPixel(0, 0, new Color(0.8f, 0.2f, 0.2f, 1f)); // Đỏ đô
            _titleTexture.Apply();

            _boxStyle = new GUIStyle(GUI.skin.box);
            _boxStyle.normal.background = _bgTexture;

            _titleStyle = new GUIStyle(GUI.skin.label);
            _titleStyle.fontSize = 18;
            _titleStyle.fontStyle = FontStyle.Bold;
            _titleStyle.normal.textColor = Color.white;
            _titleStyle.alignment = TextAnchor.MiddleCenter;

            _labelStyle = new GUIStyle(GUI.skin.label);
            _labelStyle.fontSize = 14;
            _labelStyle.normal.textColor = Color.white;

            _toggleStyle = new GUIStyle(GUI.skin.toggle);
            _toggleStyle.fontSize = 14;
            _toggleStyle.normal.textColor = Color.white;
            _toggleStyle.onNormal.textColor = Color.green;

            _buttonStyle = new GUIStyle(GUI.skin.button);
            _buttonStyle.fontSize = 14;
            _buttonStyle.fontStyle = FontStyle.Bold;
        }

        void OnGUI()
        {
            if (!_showMenu) return;
            _menuRect = GUI.Window(0, _menuRect, DrawMenuWindow, "");
        }

        void DrawMenuWindow(int windowID)
        {
            // Vẽ nền
            GUI.Box(new Rect(0, 0, _menuRect.width, _menuRect.height), "", _boxStyle);

            // Vẽ Tiêu đề
            GUI.DrawTexture(new Rect(0, 0, _menuRect.width, 40), _titleTexture);
            GUI.Label(new Rect(0, 5, _menuRect.width, 30), "AIM ASSIST & ANTIBAN", _titleStyle);

            GUILayout.Space(50);

            // --- CÁC TÍNH NĂNG ---
            EnableAimLock = GUILayout.Toggle(EnableAimLock, " Bật AimLock (Hitbox Đầu x3)", _toggleStyle);
            GUILayout.Space(10);
            
            AimHeadNeck = GUILayout.Toggle(AimHeadNeck, " Chế độ Aim Đầu + Cổ (Bone)", _toggleStyle);
            GUILayout.Space(10);

            AntiBan = GUILayout.Toggle(AntiBan, " Chặn KillCam Report (Anti-Ban)", _toggleStyle);
            GUILayout.Space(10);

            StealthMode = GUILayout.Toggle(StealthMode, " Chế độ Tàng Hình (Chống quét)", _toggleStyle);
            GUILayout.Space(20);

            // --- THANH TRƯỢT ---
            GUILayout.Label($"Kích thước Hitbox: {HitboxSize:F2}m", _labelStyle);
            HitboxSize = GUILayout.HorizontalSlider(HitboxSize, 0.5f, 3.0f);
            GUILayout.Space(10);

            GUILayout.Label($"Độ mượt (Smooth): {AimSmooth:F1}", _labelStyle);
            AimSmooth = GUILayout.HorizontalSlider(AimSmooth, 5f, 80f);

            GUILayout.Space(25);

            // Nút Đóng
            if (GUILayout.Button("ĐÓNG MENU (Hoặc nhấp 4 lần)", _buttonStyle))
                _showMenu = false;

            GUI.DragWindow(new Rect(0, 0, _menuRect.width, 40));
        }

        // --- CÁC HÀM LẤY XƯƠNG ---
        private Transform GetHeadTarget(GameObject obj)
        {
            Type playerType = Type.GetType("COW.GamePlay.Player, Assembly-CSharp");
            if (playerType != null)
            {
                Component comp = obj.GetComponent(playerType);
                if (comp != null)
                {
                    // Ưu tiên lấy HeadBoneTransform
                    MethodInfo m = playerType.GetMethod("get_HeadBoneTransform");
                    if (m != null) return m.Invoke(comp, null) as Transform;

                    // Fallback sang HeadCollider
                    m = playerType.GetMethod("get_HeadCollider");
                    if (m != null) return m.Invoke(comp, null) as Transform;
                }
            }
            return FindBone(obj.transform, "Head");
        }

        private Transform GetHeadNeckTarget(GameObject obj)
        {
            Type playerType = Type.GetType("COW.GamePlay.Player, Assembly-CSharp");
            if (playerType != null)
            {
                Component comp = obj.GetComponent(playerType);
                if (comp != null)
                {
                    // Kết hợp Đầu và Cột sống (Spine) để tạo vùng Cổ
                    MethodInfo headM = playerType.GetMethod("get_HeadBoneTransform");
                    MethodInfo spineM = playerType.GetMethod("get_SpineBoneTransform");
                    
                    Transform head = headM?.Invoke(comp, null) as Transform;
                    Transform spine = spineM?.Invoke(comp, null) as Transform;

                    if (head != null && spine != null)
                    {
                        // Tạo một Transform ảo ở giữa Đầu và Cột sống
                        GameObject go = new GameObject("AimNeckTarget");
                        go.transform.position = Vector3.Lerp(head.position, spine.position, 0.5f);
                        return go.transform;
                    }
                    return head; 
                }
            }
            return FindBone(obj.transform, "Neck") ?? FindBone(obj.transform, "Head");
        }

        private Transform FindBone(Transform root, string boneName)
        {
            if (root.name.ToLower().Contains(boneName.ToLower())) return root;
            foreach (Transform child in root)
            {
                Transform result = FindBone(child, boneName);
                if (result != null) return result;
            }
            return null;
        }
    }

    // --- CLASS PATCH CHẶN BÁO CÁO (ANTI-BAN) ---
    public class KillCamPatch
    {
        [IFix.Patch]
        public static void SetReportData_Patch(object __instance, object data) { }

        [IFix.Patch]
        public static object GetReportData_Patch(object __instance) { return null; }

        [IFix.Patch]
        public static object __Gen_Wrap_6865_Patch(object __instance, object P0) { return null; }
    }
}
