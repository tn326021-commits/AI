using System;
using System.Collections.Generic;
using UnityEngine;
using IFix;
using COW;

namespace AimAssistMod
{
    public class AimAssist
    {
        // --- CẤU HÌNH CƠ BẢN ---
        public static float MaxDistance = 200.0f;     
        public static LayerMask TargetLayer = -1;     

        // --- CẤU HÌNH TĂNG HITBOX ĐẦU (BẮN NGOÀI VẪN TRÚNG) ---
        public static float HeadHitboxRadius = 0.6f;  // BÁN KÍNH VÙNG ẢO (0.6m là rất to, dễ dính)
        public static float HeadOffsetY = 0.15f;      // Đẩy tâm lên đỉnh đầu
        public static float FOV_Hitbox = 15.0f;       // Góc quét mở rộng (độ) để tìm mục tiêu

        private static Camera _mainCam;
        private static Transform _playerTransform;

        [IFix.Patch]
        public static void Start_Patch(GameObject __instance)
        {
            _mainCam = Camera.main;
        }

        // Hàm này xử lý việc "Hút Tâm" (Magnetic Aim) khi kéo tâm
        [IFix.Patch]
        public static void LateUpdate_Patch(GameObject __instance)
        {
            if (_mainCam == null) _mainCam = Camera.main;
            if (_playerTransform == null)
            {
                GameObject p = GameObject.FindWithTag("Player");
                if (p != null) _playerTransform = p.transform;
                else if (_mainCam != null) _playerTransform = _mainCam.transform.root;
            }

            if (_mainCam == null || _playerTransform == null) return;

            Ray ray = _mainCam.ScreenPointToRay(new Vector3(Screen.width / 2f, Screen.height / 2f, 0f));
            Vector3 rawAimDir = ray.direction;
            bool isPulling = IsPullingAim();

            // Tìm mục tiêu với Hitbox siêu to
            Vector3 hitPoint;
            if (TryGetExpandedHeadHitbox(_playerTransform.position, rawAimDir, isPulling, out hitPoint))
            {
                // Nếu tìm thấy, xoay Camera hút vào điểm ảo đó (chỉ khi kéo tâm)
                if (isPulling)
                {
                    Vector3 targetDir = (hitPoint - _mainCam.transform.position).normalized;
                    Quaternion targetRot = Quaternion.LookRotation(targetDir);
                    _mainCam.transform.rotation = Quaternion.Slerp(_mainCam.transform.rotation, targetRot, Time.deltaTime * 30f);
                }
            }
        }

        // Hàm này dùng để "Bẻ lái đạn" (Silent Aim) - Bạn cần gọi nó ở hàm bắn của game
        // Hãy tìm hàm Fire/Shoot trong Assembly-CSharp.dll và patch nó
        public static Vector3 GetSilentAimDirection(Vector3 originalDir)
        {
            if (!IsPullingAim()) return originalDir;

            Vector3 hitPoint;
            if (TryGetExpandedHeadHitbox(_playerTransform.position, originalDir, true, out hitPoint))
            {
                // Đạn sẽ bay thẳng vào cái Hitbox ảo to đùng này, bất chấp tâm ngắm lệch
                return (hitPoint - _mainCam.transform.position).normalized;
            }
            return originalDir;
        }

        private static bool TryGetExpandedHeadHitbox(Vector3 playerPos, Vector3 aimDir, bool isPulling, out Vector3 hitPoint)
        {
            hitPoint = Vector3.zero;
            Collider[] targets = Physics.OverlapSphere(playerPos, MaxDistance, TargetLayer);
            
            Transform bestTarget = null;
            float bestScore = float.MaxValue;

            foreach (var col in targets)
            {
                if (col.transform == _playerTransform) continue;

                // Tìm xương đầu
                Transform head = FindBone(col.transform, "Head") ?? FindBone(col.transform, "head");
                if (head == null) continue;

                // TÂM ĐẦU THỰC TẾ + OFFSET
                Vector3 headCenter = head.position + (Vector3.up * HeadOffsetY);
                Vector3 toHead = headCenter - playerPos;

                // 1. Tính góc lệch
                float angle = Vector3.Angle(aimDir, toHead);
                
                // 2. Tính khoảng cách vuông góc từ tâm ngắm đến tâm đầu
                float distToRay = Vector3.Cross(aimDir, toHead.normalized).magnitude * toHead.magnitude;

                // NẾU TÂM NGẮM LƯỚT QUA VÙNG ẢO (BÁN KÍNH 0.6M) -> TÍNH LÀ TRÚNG
                bool isInsideHitbox = distToRay <= HeadHitboxRadius;
                bool isInsideFOV = angle <= FOV_Hitbox;

                if (isInsideHitbox || (isPulling && isInsideFOV))
                {
                    // Ưu tiên mục tiêu gần tâm ngắm nhất
                    float score = distToRay + (toHead.magnitude * 0.01f); 
                    if (score < bestScore)
                    {
                        bestScore = score;
                        bestTarget = head;
                        hitPoint = headCenter; // Trả về tâm của cái đầu ảo
                    }
                }
            }

            return bestTarget != null;
        }

        private static bool IsPullingAim()
        {
            return Input.GetMouseButton(1); 
        }

        private static Transform FindBone(Transform root, string boneName)
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
}
