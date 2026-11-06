using System;
using UnityEngine;
using IFix;
using COW;

namespace AimAssistMod
{
    public class UGCPlayerRepItemPatch
    {
        // Vá hàm get_HeadBonesScale để trả về Scale x3
        [IFix.Patch]
        public static Vector3 get_HeadBonesScale_Patch(UGCPlayerRepItem __instance)
        {
            // Gọi hàm gốc để lấy giá trị cũ, sau đó nhân 3
            Vector3 originalScale = __instance.get_HeadBonesScale();
            return originalScale * 3.0f;
        }

        // Nếu bạn muốn sát thương đầu không bị giảm (UGC mode)
        [IFix.Patch]
        public static float get_UGCHeadshotDamageDecreaseScale_Patch(UGCPlayerRepItem __instance)
        {
            // Trả về 1.0f (tức là 100% sát thương, không bị giảm)
            return 1.0f; 
        }
    }
}
