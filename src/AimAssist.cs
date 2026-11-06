using System;
using System.Reflection;
using UnityEngine;

namespace AimAssistMod
{
    public class AimAssist
    {
        public static void Init()
        {
            GameObject go = new GameObject("AimAssistRunner");
            UnityEngine.Object.DontDestroyOnLoad(go);
            go.AddComponent<AimAssistRunner>();
        }
    }

    public class AimAssistRunner : MonoBehaviour
    {
        void Update()
        {
            GameObject player = GameObject.FindWithTag("Player");
            if (player == null) return;

            Camera cam = Camera.main;
            if (cam == null) return;

            if (!Input.GetMouseButton(1)) return;

            Ray ray = cam.ScreenPointToRay(new Vector3(Screen.width / 2f, Screen.height / 2f, 0f));
            Vector3 aimDir = ray.direction;

            Collider[] targets = Physics.OverlapSphere(player.transform.position, 200f);
            Transform bestHead = null;
            float bestScore = float.MaxValue;

            foreach (var col in targets)
            {
                if (col.transform.root == player.transform) continue;

                Transform head = GetHeadCollider(col.gameObject);
                if (head == null) continue;

                Vector3 toHead = head.position - player.transform.position;
                float distToRay = Vector3.Cross(aimDir, toHead.normalized).magnitude * toHead.magnitude;

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

            if (bestHead != null)
            {
                Vector3 targetDir = (bestHead.position - cam.transform.position).normalized;
                Quaternion targetRot = Quaternion.LookRotation(targetDir);
                cam.transform.rotation = Quaternion.Slerp(cam.transform.rotation, targetRot, Time.deltaTime * 30f);
            }
        }

        private Transform GetHeadCollider(GameObject obj)
        {
            Type playerType = Type.GetType("COW.GamePlay.Player, Assembly-CSharp");
            if (playerType != null)
            {
                Component playerComp = obj.GetComponent(playerType);
                if (playerComp != null)
                {
                    MethodInfo method = playerType.GetMethod("get_HeadCollider", BindingFlags.Public | BindingFlags.Instance);
                    if (method != null)
                    {
                        return method.Invoke(playerComp, null) as Transform;
                    }
                }
            }
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
