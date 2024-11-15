using UnityEngine;

public class AssignMaterialToPlanes : MonoBehaviour
{
    public Material newMaterial;

    void Start()
    {
        foreach (Transform child in transform)
        {
            MeshRenderer renderer = child.GetComponent<MeshRenderer>();
            if (renderer != null)
            {
                renderer.material = newMaterial;
            }
        }
    }
}
