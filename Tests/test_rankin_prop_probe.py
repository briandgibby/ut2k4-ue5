"""Contract checks for the single native Brace01HA triangle export."""

from pathlib import Path
import unittest

try:
    from Tools.rankin_prop_probe import parse_triangles
except ModuleNotFoundError:
    parse_triangles = None


SOURCE = Path(__file__).resolve().parents[1] / "Exports/Rankin/MeshT3DProbe/Beams.Brace01HA.t3d"


class RankinPropProbeTests(unittest.TestCase):
    def triangles(self):
        self.assertIsNotNone(parse_triangles, "The native triangle reader is not implemented")
        return parse_triangles(SOURCE.read_text(encoding="utf-8"))

    def test_recovers_all_288_triangles(self):
        triangles = self.triangles()
        self.assertEqual(len(triangles), 288)
        self.assertTrue(all(len(triangle["vertices"]) == 3 for triangle in triangles))

    def test_preserves_source_positions_and_dimensions(self):
        triangles = self.triangles()
        vertices = [vertex for triangle in triangles for vertex in triangle["vertices"]]
        self.assertEqual(vertices[0][:3], (-193.415009, -63.636997, -5.45))
        lower = [min(vertex[axis] for vertex in vertices) for axis in range(3)]
        upper = [max(vertex[axis] for vertex in vertices) for axis in range(3)]
        self.assertEqual(lower, [-264.000977, -72.977997, -57.874001])
        self.assertEqual(upper, [248.0, 73.759995, 57.547001])
        for actual, expected in zip(
            [upper[axis] - lower[axis] for axis in range(3)],
            [512.000977, 146.737992, 115.421002],
        ):
            self.assertAlmostEqual(actual, expected, places=6)

    def test_preserves_uvs_including_values_outside_zero_to_one(self):
        triangles = self.triangles()
        vertices = [vertex for triangle in triangles for vertex in triangle["vertices"]]
        self.assertTrue(all(len(vertex) == 5 for vertex in vertices))
        self.assertEqual(triangles[0]["vertices"][0][3:], (0.647563, 1.134639))
        self.assertEqual(triangles[1]["vertices"][2][3:], (0.163306, -0.784004))
        self.assertEqual(triangles[-1]["vertices"][1][3:], (0.664441, 1.119658))
        self.assertEqual([min(vertex[axis] for vertex in vertices) for axis in (3, 4)], [0.162121, -0.784004])
        self.assertEqual([max(vertex[axis] for vertex in vertices) for axis in (3, 4)], [0.883801, 1.169667])

    def test_covers_every_triangle_with_the_source_material_and_mask(self):
        triangles = self.triangles()
        self.assertEqual({triangle["material"] for triangle in triangles}, {"HumanoidArchitecture.Bases.bas05bHA"})
        self.assertEqual({triangle["smoothing_mask"] for triangle in triangles}, {1})

    def test_rejects_an_incomplete_triangle(self):
        self.assertIsNotNone(parse_triangles, "The native triangle reader is not implemented")
        incomplete = """Begin Triangle
Texture HumanoidArchitecture.Bases.bas05bHA
SmoothingMask 1
Vertex 0 -193.415009 -63.636997 -5.450000 0.647563 1.134639
Vertex 1 -189.950012 59.024002 -42.521000 0.508546 0.674660
End Triangle
"""
        with self.assertRaisesRegex(ValueError, "Incomplete triangle"):
            parse_triangles(incomplete)


if __name__ == "__main__":
    unittest.main()
