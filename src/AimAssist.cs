using System;
using System.Reflection;
using UnityEngine;

namespace AimAssistMod
{
    public class AimAssist
    {
        // Hàm này sẽ được gọi tự động khi game load (thông qua một hook nào đó)
        // Hoặc chúng ta sẽ dùng Reflection để gắn nó vào Player
        public static void Init()
        {
            Debug.Log("[AimAssist] Mod đã được nạp!");
            
            // Tạo một GameObject ảo để chạy Update
            GameObject go = new GameObject("AimAssistRunner");
            UnityEngine.Object.DontDestroyOnLoad(go);
            go.AddComponent<AimAssistRunner>();
        }
    }

    public class AimAssistRunner : MonoBehaviour
    {
        void Update()
        {
            // 1. Tìm Player
            GameObject player = GameObject.FindWithTag("Player");
            if (player == null) return;

            Camera cam = Camera.main;
            if (cam == null) return;

            // 2. Chỉ hút tâm khi kéo chuột phải
            if (!Input.GetMouseButton(1)) return;

            // 3. Quét mục tiêu
            Ray ray = cam.ScreenPointToRay(new Vector3(Screen.width / 2f, Screen.height / 2f, 0f));
            Vector3 aimDir = ray.direction;

            Collider[] targets = Physics.OverlapSphere(player.transform.position, 200f);
            Transform bestHead = null;
            float bestScore = float.MaxValue;

            foreach (var col in targets)
            {
                if (col.transform.root == player.transform) continue;

                // Dùng Reflection để lấy hàm get_HeadCollider của game
                // (Vì chúng ta thấy nó có trong file patch)
                Transform head = GetHeadCollider(col.gameObject);
                if (head == null) continue;

                Vector3 toHead = head.position - player.transform.position;
                float distToRay = Vector3.Cross(aimDir, toHead.normalized).magnitude * toHead.magnitude;

                // Hitbox ảo bán kính 0.8 mét
                if (distToRay <= 0.8f)
                {
                    float score = distToRay + (toHead.magnitude * 0.01f);
                    if (score < bestScore)
                    {
                        bestScore = score;
                        bestHead = head;
                    }
                }
            }

            // 4. Hút tâm vào đầu
            if (bestHead != null)
            {
                Vector3 targetDir = (bestHead.position - cam.transform.position).normalized;
                Quaternion targetRot = Quaternion.LookRotation(targetDir);
                cam.transform.rotation = Quaternion.Slerp(cam.transform.rotation, targetRot, Time.deltaTime * 30f);
            }
        }

        // Hàm lấy HeadCollider thông qua Reflection
        private Transform GetHeadCollider(GameObject obj)
        {
            // Tìm component Player của game (dựa trên tên class COW.GamePlay.Player)
            Type playerType = Type.GetType("COW.GamePlay.Player, Assembly-CSharp");
            if (playerType != null)
            {
                Component playerComp = obj.GetComponent(playerType);
                if (playerComp != null)
                {
                    // Gọi hàm get_HeadCollider
                    MethodInfo method = playerType.GetMethod("get_HeadCollider", BindingFlags.Public | BindingFlags.Instance);
                    if (method != null)
                    {
                        return method.Invoke(playerComp, null) as Transform;
                    }
                }
            }
            
            // Nếu không tìm thấy, thử tìm xương bằng tên
            return FindBone(obj.transform, "Head") ?? FindBone(obj.transform, "head");
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
}
