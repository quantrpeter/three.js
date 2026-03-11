from manim import *
import numpy as np

SPACE_BG = "#020810"
ACCENT = "#4488ff"
SOFT = "#b0d4ff"
SHIP_COL = "#ff9c7c"
TANK_COL = "#7cff7c"
ROBOT_COL = "#7cacff"


class Lesson18(Scene):
    def construct(self):
        self.camera.background_color = SPACE_BG
        self.title_card()
        self.overview()
        self.scene_setup()
        self.starfield()
        self.planet_creation()
        self.unit_system()
        self.raycasting_placement()
        self.surface_orientation()
        self.interaction_flow()
        self.outro()

    # ── helpers ───────────────────────────────────────────────

    def section_header(self, text):
        title = Text(text, font_size=36, color=ACCENT)
        line = Line(LEFT * 3, RIGHT * 3, color=ACCENT, stroke_width=2)
        line.next_to(title, DOWN, buff=0.15)
        grp = VGroup(title, line)
        self.play(FadeIn(grp, shift=UP * 0.3))
        self.wait(0.8)
        self.play(FadeOut(grp))

    def mono(self, text, font_size=14):
        return Text(text, font_size=font_size, color=SOFT, font="Menlo")

    # ── 1  title ─────────────────────────────────────────────

    def title_card(self):
        np.random.seed(42)
        stars = VGroup(*[
            Dot(
                point=[np.random.uniform(-7, 7),
                       np.random.uniform(-4, 4), 0],
                radius=np.random.uniform(0.01, 0.03),
                color=WHITE,
            ).set_opacity(np.random.uniform(0.3, 0.9))
            for _ in range(80)
        ])
        self.play(FadeIn(stars, run_time=1.5))

        lesson = Text("LESSON 18", font_size=24, color=SOFT)
        title = Text("Planetary Annihilation RTS", font_size=48, color=WHITE)
        subtitle = Text(
            "Building an Interactive 3D Strategy Game with Three.js",
            font_size=20, color=SOFT,
        )
        group = VGroup(lesson, title, subtitle).arrange(DOWN, buff=0.3)

        planet = Circle(
            radius=0.6, color="#2266aa",
            fill_opacity=0.3, stroke_width=2,
        )
        atmos = Circle(
            radius=0.65, color=ACCENT,
            fill_opacity=0.05, stroke_width=1,
        )
        planet_grp = VGroup(planet, atmos).next_to(group, LEFT, buff=0.8)

        self.play(Write(lesson, run_time=0.6), Write(title, run_time=1.2))
        self.play(
            FadeIn(subtitle, shift=UP * 0.2),
            GrowFromCenter(planet_grp),
        )
        self.wait(2)
        self.play(FadeOut(VGroup(stars, group, planet_grp)))

    # ── 2  overview ──────────────────────────────────────────

    def overview(self):
        self.section_header("What We're Building")

        items = [
            "A planet with procedural terrain vertex colors",
            "A 5,000-star spherical background",
            "Three unit types  -  Ship / Tank / Robot",
            "Click-to-place units via raycasting",
            "Quaternion-based surface orientation",
        ]
        bullets = VGroup()
        for text in items:
            dot = Dot(radius=0.05, color=ACCENT)
            txt = Text(text, font_size=20, color=SOFT)
            row = VGroup(dot, txt).arrange(RIGHT, buff=0.25)
            bullets.add(row)
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(ORIGIN)

        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.3)
        self.wait(1.5)
        self.play(FadeOut(bullets))

    # ── 3  scene architecture ────────────────────────────────

    def scene_setup(self):
        self.section_header("1   Scene Architecture")

        data = [
            ("Camera",   "#3366cc", "PerspectiveCamera\nFOV 45"),
            ("Scene",    "#2a5a2a", "Background #020810"),
            ("Renderer", "#8b4513", "WebGLRenderer\nACES Filmic"),
            ("Controls", "#6a3d7d", "OrbitControls\nDamping 0.08"),
        ]
        boxes = VGroup()
        box_map = {}
        for name, col, desc in data:
            box = RoundedRectangle(
                corner_radius=0.15, width=2.5, height=1.4,
                fill_color=col, fill_opacity=0.3,
                stroke_color=col, stroke_width=2,
            )
            label = Text(name, font_size=18, color=WHITE)
            detail = Text(desc, font_size=12, color=SOFT)
            VGroup(label, detail).arrange(DOWN, buff=0.1).move_to(box)
            g = VGroup(box, label, detail)
            boxes.add(g)
            box_map[name] = g

        boxes.arrange_in_grid(rows=2, cols=2, buff=0.4).move_to(UP * 0.3)

        self.play(LaggedStart(
            *[FadeIn(b, scale=0.8) for b in boxes],
            lag_ratio=0.2,
        ))
        self.wait(1)

        arrows = VGroup(
            Arrow(
                box_map["Camera"].get_right(),
                box_map["Controls"].get_left(),
                buff=0.15, color=ACCENT, stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            ),
            Arrow(
                box_map["Scene"].get_right(),
                box_map["Renderer"].get_left(),
                buff=0.15, color=ACCENT, stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            ),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3))
        self.wait(0.5)

        light_title = Text("Three-Light Rig", font_size=20, color=ACCENT)
        lights = VGroup(
            Text("Ambient   -  soft fill, intensity 1.5", font_size=14, color=SOFT),
            Text("Sun       -  directional, intensity 2.5 + shadows",
                 font_size=14, color=SOFT),
            Text("Rim       -  blue backlight, intensity 0.8",
                 font_size=14, color=SOFT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        light_grp = VGroup(light_title, lights).arrange(DOWN, buff=0.25)
        light_grp.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(light_grp, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(boxes, arrows, light_grp)))

    # ── 4  starfield ─────────────────────────────────────────

    def starfield(self):
        self.section_header("2   Starfield Generation")

        header = Text("Spherical to Cartesian", font_size=22, color=WHITE)
        header.to_edge(UP, buff=0.6)

        eqs = VGroup(
            Text("\u03b8 = rand \u00d7 2\u03c0", font_size=24, color=SOFT),
            Text("\u03c6 = arccos(2 \u00b7 rand \u2212 1)", font_size=24, color=SOFT),
            Text("r = 80 + rand \u00d7 120", font_size=24, color=SOFT),
        ).arrange(DOWN, buff=0.25).next_to(header, DOWN, buff=0.4)

        xyz = VGroup(
            Text("x = r \u00b7 sin\u03c6 \u00b7 cos\u03b8", font_size=22, color=ACCENT),
            Text("y = r \u00b7 sin\u03c6 \u00b7 sin\u03b8", font_size=22, color=ACCENT),
            Text("z = r \u00b7 cos\u03c6", font_size=22, color=ACCENT),
        ).arrange(DOWN, buff=0.2).next_to(eqs, DOWN, buff=0.5)

        self.play(Write(header))
        self.play(LaggedStart(
            *[FadeIn(e, shift=RIGHT * 0.3) for e in eqs], lag_ratio=0.3,
        ))
        self.wait(0.8)
        self.play(LaggedStart(
            *[FadeIn(c, shift=LEFT * 0.3) for c in xyz], lag_ratio=0.3,
        ))
        self.wait(1.5)
        self.play(FadeOut(VGroup(header, eqs, xyz)))

        note = Text(
            "5,000 stars on a spherical shell  (r = 80 .. 200)",
            font_size=18, color=SOFT,
        )
        note.to_edge(UP, buff=0.5)
        self.play(FadeIn(note))

        inner = Circle(
            radius=1.5, color=ACCENT,
            stroke_width=1, stroke_opacity=0.3,
        )
        outer = Circle(
            radius=2.5, color=ACCENT,
            stroke_width=1, stroke_opacity=0.3,
        )
        rl_in = Text("r=80", font_size=12, color=SOFT).next_to(inner, RIGHT, buff=0.1)
        rl_out = Text("r=200", font_size=12, color=SOFT).next_to(outer, RIGHT, buff=0.1)
        self.play(Create(inner), Create(outer), FadeIn(rl_in), FadeIn(rl_out))

        np.random.seed(123)
        dots = VGroup(*[
            Dot(
                [
                    (1.5 + np.random.random()) * np.cos(np.random.random() * TAU),
                    (1.5 + np.random.random()) * np.sin(np.random.random() * TAU),
                    0,
                ],
                radius=0.015, color=WHITE,
            ).set_opacity(np.random.uniform(0.4, 1.0))
            for _ in range(200)
        ])
        self.play(LaggedStart(
            *[FadeIn(d, scale=0.5) for d in dots],
            lag_ratio=0.005, run_time=2,
        ))
        self.wait(1.5)
        self.play(FadeOut(VGroup(note, inner, outer, rl_in, rl_out, dots)))

    # ── 5  planet ────────────────────────────────────────────

    def planet_creation(self):
        self.section_header("3   Procedural Planet")

        sphere = Circle(
            radius=1.5, color="#2266aa",
            fill_opacity=0.6, stroke_width=2,
        )
        sphere.shift(LEFT * 3)
        s_label = Text(
            "SphereGeometry(3, 128, 128)",
            font_size=13, color=SOFT,
        )
        s_label.next_to(sphere, DOWN, buff=0.3)
        self.play(GrowFromCenter(sphere), FadeIn(s_label))

        box = RoundedRectangle(
            corner_radius=0.15, width=5.2, height=3.2,
            fill_color="#0a1a30", fill_opacity=0.8,
            stroke_color=ACCENT, stroke_width=1,
        ).shift(RIGHT * 2)

        box_title = Text("Vertex Color Logic", font_size=18, color=ACCENT)
        code = self.mono(
            "noise  = sin(4x)*cos(3y)*sin(5z)\n"
            "noise2 = sin(12x + 8y) * 0.15\n"
            "val    = noise + noise2\n"
            "\n"
            "val > 0.6   ->  Green  (land)\n"
            "val > 0.4   ->  Brown  (terrain)\n"
            "else        ->  Blue   (water)",
            font_size=13,
        )
        VGroup(box_title, code).arrange(DOWN, buff=0.25).move_to(box)

        self.play(FadeIn(box), Write(box_title))
        self.play(FadeIn(code, shift=UP * 0.2))
        self.wait(2)

        legend = VGroup(*[
            VGroup(
                Square(
                    side_length=0.25, fill_color=c,
                    fill_opacity=1, stroke_width=0,
                ),
                Text(l, font_size=14, color=SOFT),
            ).arrange(RIGHT, buff=0.15)
            for l, c in [
                ("Water",   "#1a3a5a"),
                ("Terrain", "#5a4030"),
                ("Land",    "#2a5a2a"),
            ]
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.next_to(sphere, RIGHT, buff=0.3).shift(UP * 0.3)
        self.play(FadeIn(legend))

        atmos = Circle(
            radius=1.58, color=ACCENT,
            fill_opacity=0.08, stroke_width=1, stroke_opacity=0.3,
        )
        atmos.move_to(sphere)
        a_note = Text(
            "Atmosphere layer:  radius * 1.02,  opacity 0.08",
            font_size=14, color=SOFT,
        )
        a_note.to_edge(DOWN, buff=0.5)
        self.play(Create(atmos), FadeIn(a_note))
        self.wait(2)
        self.play(FadeOut(VGroup(
            sphere, s_label, box, box_title, code, legend, atmos, a_note,
        )))

    # ── 6  units ─────────────────────────────────────────────

    def unit_system(self):
        self.section_header("4   Unit Types")

        units = [
            ("Ship",  SHIP_COL,
             "STL model loaded\nvia STLLoader",
             "Centered + scaled 0.06\nMeshStandardMaterial"),
            ("Tank",  TANK_COL,
             "Box body + cylinder\nturret + barrel",
             "2 track geometries\n5 primitives total"),
            ("Robot", ROBOT_COL,
             "Torso + head\n+ red emissive visor",
             "2 legs + 2 arms\n7 primitives total"),
        ]
        cards = VGroup()
        for name, col, desc, detail in units:
            card = RoundedRectangle(
                corner_radius=0.15, width=3.5, height=3.0,
                fill_color="#0a1530", fill_opacity=0.8,
                stroke_color=col, stroke_width=2,
            )
            t = Text(name, font_size=24, color=col)
            d = Text(desc, font_size=14, color=SOFT)
            dt = Text(detail, font_size=12, color=WHITE).set_opacity(0.6)
            VGroup(t, d, dt).arrange(DOWN, buff=0.3).move_to(card)
            cards.add(VGroup(card, t, d, dt))
        cards.arrange(RIGHT, buff=0.4).move_to(UP * 0.3)

        self.play(LaggedStart(
            *[FadeIn(c, scale=0.85) for c in cards], lag_ratio=0.3,
        ))
        self.wait(2)

        mat = Text(
            "All use MeshStandardMaterial  { roughness, metalness, emissive }",
            font_size=16, color=SOFT,
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(mat, shift=UP * 0.2))
        self.wait(1.5)

        geom_note = Text(
            "Each unit is a THREE.Group containing child meshes",
            font_size=15, color=ACCENT,
        ).next_to(mat, UP, buff=0.3)
        self.play(FadeIn(geom_note))
        self.wait(1.5)
        self.play(FadeOut(VGroup(cards, mat, geom_note)))

    # ── 7  raycasting ────────────────────────────────────────

    def raycasting_placement(self):
        self.section_header("5   Raycasting & Placement")

        cam = RoundedRectangle(
            corner_radius=0.1, width=1.2, height=0.8,
            fill_color="#3366cc", fill_opacity=0.4,
            stroke_color="#3366cc", stroke_width=2,
        ).shift(LEFT * 5 + UP * 1.5)
        cam_l = Text("Camera", font_size=14, color=SOFT)
        cam_l.next_to(cam, DOWN, buff=0.1)

        screen = Rectangle(
            width=0.7, height=0.7,
            fill_color="#1a1a2e", fill_opacity=0.6,
            stroke_color=ACCENT, stroke_width=1,
        ).shift(LEFT * 3 + UP * 0.5)
        scr_l = Text("Mouse", font_size=11, color=SOFT)
        scr_l.next_to(screen, DOWN, buff=0.1)
        mdot = Dot(screen.get_center(), radius=0.05, color="#ff4444")

        planet_c = Circle(
            radius=1.2, color="#2266aa",
            fill_opacity=0.4, stroke_width=2,
        ).shift(RIGHT * 1.5)
        pl_l = Text("Planet", font_size=14, color=SOFT)
        pl_l.next_to(planet_c, DOWN, buff=0.2)

        self.play(
            FadeIn(cam), FadeIn(cam_l),
            FadeIn(screen), FadeIn(scr_l), FadeIn(mdot),
            GrowFromCenter(planet_c), FadeIn(pl_l),
        )

        hit_pt = planet_c.get_left() + RIGHT * 0.3
        ray = DashedLine(
            cam.get_center(), hit_pt,
            dash_length=0.1, color="#ff6644", stroke_width=2,
        )
        ray_l = Text("Raycaster", font_size=12, color="#ff6644")
        ray_l.next_to(ray, UP, buff=0.1)
        self.play(Create(ray), FadeIn(ray_l))

        hit = Dot(hit_pt, radius=0.08, color=YELLOW)
        hit_l = Text("hit.point", font_size=12, color=YELLOW)
        hit_l.next_to(hit, UR, buff=0.1)

        direction = hit_pt - planet_c.get_center()
        direction = direction / np.linalg.norm(direction) * 0.7
        norm_arr = Arrow(
            hit_pt, hit_pt + direction,
            buff=0, color="#00ff88", stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )
        norm_l = Text("face.normal", font_size=12, color="#00ff88")
        norm_l.next_to(norm_arr.get_end(), UP, buff=0.1)

        self.play(FadeIn(hit, scale=2), FadeIn(hit_l))
        self.play(GrowArrow(norm_arr), FadeIn(norm_l))
        self.wait(1)

        step_box = RoundedRectangle(
            corner_radius=0.1, width=5, height=2.2,
            fill_color="#0a0a1a", fill_opacity=0.9,
            stroke_color=ACCENT, stroke_width=1,
        ).shift(RIGHT * 3.5 + UP * 1.5)

        steps = VGroup(
            Text("1. Mouse -> NDC coords", font_size=13, color=SOFT),
            Text("2. raycaster.setFromCamera(mouse, camera)",
                 font_size=13, color=SOFT),
            Text("3. intersects = raycaster.intersectObject(planet)",
                 font_size=13, color=SOFT),
            Text("4. Extract point + face normal from hit",
                 font_size=13, color=SOFT),
            Text("5. Place unit at intersection",
                 font_size=13, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(step_box)

        self.play(FadeIn(step_box))
        self.play(LaggedStart(
            *[FadeIn(s, shift=RIGHT * 0.2) for s in steps],
            lag_ratio=0.2,
        ))
        self.wait(2)

        ndc_note = self.mono(
            "mouse.x = (clientX / width)  * 2 - 1\n"
            "mouse.y = (clientY / height) * -2 + 1",
            font_size=12,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(ndc_note))
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            cam, cam_l, screen, scr_l, mdot,
            planet_c, pl_l, ray, ray_l,
            hit, hit_l, norm_arr, norm_l,
            step_box, steps, ndc_note,
        )))

    # ── 8  surface orientation ───────────────────────────────

    def surface_orientation(self):
        self.section_header("6   Surface Orientation")

        planet_c = Circle(
            radius=2, color="#2266aa",
            fill_opacity=0.2, stroke_width=2,
        ).shift(LEFT * 1)
        self.play(GrowFromCenter(planet_c))

        angles = [30, 80, 150, 220, 300]
        normals = VGroup()
        units_v = VGroup()
        for a in angles:
            rad = np.radians(a)
            cx, cy = planet_c.get_center()[0], planet_c.get_center()[1]
            px = cx + 2 * np.cos(rad)
            py = cy + 2 * np.sin(rad)
            nx = np.cos(rad) * 0.5
            ny = np.sin(rad) * 0.5
            arr = Arrow(
                [px, py, 0], [px + nx, py + ny, 0],
                buff=0, color="#00ff88", stroke_width=2,
                max_tip_length_to_length_ratio=0.25,
            )
            normals.add(arr)
            tri = RegularPolygon(
                n=3, fill_color=SHIP_COL,
                fill_opacity=0.7, stroke_width=1,
                stroke_color=SHIP_COL,
            )
            tri.scale(0.15).move_to([px, py, 0]).rotate(rad - PI / 2)
            units_v.add(tri)

        self.play(LaggedStart(
            *[GrowArrow(n) for n in normals],
            lag_ratio=0.15, run_time=1.5,
        ))
        self.play(LaggedStart(
            *[FadeIn(u, scale=0.5) for u in units_v],
            lag_ratio=0.15, run_time=1.5,
        ))
        self.wait(0.5)

        formula_box = RoundedRectangle(
            corner_radius=0.1, width=5, height=2.8,
            fill_color="#0a0a2a", fill_opacity=0.9,
            stroke_color=ACCENT, stroke_width=1,
        ).shift(RIGHT * 3)

        ft = Text("orientToSurface()", font_size=16, color=ACCENT)
        f1 = Text("up = (0, 1, 0)", font_size=20, color=SOFT)
        f1_note = Text("default up", font_size=11, color=WHITE).set_opacity(0.5)
        f1_row = VGroup(f1, f1_note).arrange(RIGHT, buff=0.3)

        f2 = Text("n = surfaceNormal", font_size=20, color="#00ff88")
        f3 = Text("q = Quaternion( up \u2192 n )", font_size=19, color=WHITE)
        f4 = Text(
            "obj.quaternion.copy(q)",
            font_size=14, color=SOFT, font="Menlo",
        )
        formulas = VGroup(ft, f1_row, f2, f3, f4).arrange(DOWN, buff=0.2)
        formulas.move_to(formula_box)

        self.play(FadeIn(formula_box), Write(ft))
        self.play(FadeIn(f1_row), FadeIn(f2))
        self.play(FadeIn(f3), FadeIn(f4))
        self.wait(2)

        note = Text(
            "Each unit's local Y-axis aligns to the planet surface normal",
            font_size=15, color=SOFT,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(
            planet_c, normals, units_v,
            formula_box, formulas, note,
        )))

    # ── 9  interaction flow ──────────────────────────────────

    def interaction_flow(self):
        self.section_header("7   Interaction Flow")

        steps = [
            ("Select",    "#3366cc", "Click menu icon\nselectedUnit = type"),
            ("Hover",     "#cc8833", "onPointerMove\nraycast -> ghost mesh"),
            ("Place",     "#33aa55", "onPointerDown\ncreateUnitMesh + orient"),
            ("Deselect",  "#aa3355", "Click same icon\nremove ghost mesh"),
        ]

        nodes = VGroup()
        for label, col, desc in steps:
            box = RoundedRectangle(
                corner_radius=0.12, width=2.4, height=1.6,
                fill_color=col, fill_opacity=0.2,
                stroke_color=col, stroke_width=2,
            )
            t = Text(label, font_size=16, color=col)
            d = Text(desc, font_size=11, color=SOFT)
            VGroup(t, d).arrange(DOWN, buff=0.15).move_to(box)
            nodes.add(VGroup(box, t, d))

        nodes.arrange(RIGHT, buff=0.5).move_to(UP * 0.8)

        self.play(LaggedStart(
            *[FadeIn(n, scale=0.85) for n in nodes], lag_ratio=0.25,
        ))

        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arr = Arrow(
                nodes[i].get_right(), nodes[i + 1].get_left(),
                buff=0.1, color=WHITE, stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            )
            arrows.add(arr)
        self.play(LaggedStart(
            *[GrowArrow(a) for a in arrows], lag_ratio=0.2,
        ))
        self.wait(1)

        ghost_box = RoundedRectangle(
            corner_radius=0.1, width=6.5, height=1.6,
            fill_color="#0a0a2a", fill_opacity=0.9,
            stroke_color=ACCENT, stroke_width=1,
        ).to_edge(DOWN, buff=0.5)

        ghost_title = Text("Ghost Preview", font_size=16, color=ACCENT)
        ghost_desc = VGroup(
            Text("Transparent clone follows cursor on planet",
                 font_size=13, color=SOFT),
            Text("material.transparent = true,  opacity = 0.5",
                 font_size=12, color=SOFT, font="Menlo"),
            Text("Removed on deselect or when cursor leaves planet",
                 font_size=13, color=SOFT),
        ).arrange(DOWN, buff=0.1)
        VGroup(ghost_title, ghost_desc).arrange(DOWN, buff=0.15).move_to(ghost_box)

        self.play(FadeIn(ghost_box), FadeIn(ghost_title), FadeIn(ghost_desc))
        self.wait(2.5)
        self.play(FadeOut(VGroup(nodes, arrows, ghost_box, ghost_title, ghost_desc)))

    # ── 10  outro ────────────────────────────────────────────

    def outro(self):
        self.section_header("Recap")

        lines = [
            "1.  Scene architecture  -  Camera + Renderer + 3-light rig",
            "2.  Starfield  -  spherical coords, 5000 points",
            "3.  Planet  -  trig-noise vertex coloring + atmosphere",
            "4.  Units  -  Ship (STL) / Tank / Robot from primitives",
            "5.  Raycasting  -  mouse ray intersects planet sphere",
            "6.  Orientation  -  quaternion aligns units to surface",
            "7.  Interaction  -  select, ghost preview, click to place",
        ]
        summary = VGroup(
            *[Text(l, font_size=17, color=SOFT) for l in lines]
        )
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(ORIGIN)

        self.play(LaggedStart(
            *[FadeIn(s, shift=RIGHT * 0.3) for s in summary],
            lag_ratio=0.12, run_time=2.5,
        ))
        self.wait(3)
        self.play(FadeOut(summary))

        end = Text("Lesson 18 Complete", font_size=40, color=WHITE)
        sub = Text("Planetary Annihilation RTS", font_size=22, color=ACCENT)
        end_grp = VGroup(end, sub).arrange(DOWN, buff=0.3)
        self.play(FadeIn(end_grp, scale=0.8))
        self.wait(2)
        self.play(FadeOut(end_grp))
