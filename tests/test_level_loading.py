"""
Testes para carregamento de níveis.
"""
import unittest
import sys
import os

# Adiciona src ao path
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")
sys.path.insert(0, src_path)


class TestLevelLoading(unittest.TestCase):
    """Testes para carregamento de níveis."""
    
    def test_level_file_exists(self):
        """Verifica se o arquivo de nível existe."""
        level_path = os.path.join(
            src_path, "rallyx_clone", "assets", "data", "level_01.json"
        )
        self.assertTrue(os.path.exists(level_path))
    
    def test_level_data_valid(self):
        """Verifica se os dados do nível são válidos."""
        import json
        
        level_path = os.path.join(
            src_path, "rallyx_clone", "assets", "data", "level_01.json"
        )
        
        with open(level_path, 'r') as f:
            data = json.load(f)
        
        # Verifica campos obrigatórios
        self.assertIn("grid", data)
        self.assertIn("player_spawn", data)
        self.assertIn("enemy_spawns", data)
        self.assertIn("flags", data)
        self.assertIn("time_limit", data)
        
        # Verifica grid
        self.assertIsInstance(data["grid"], list)
        self.assertGreater(len(data["grid"]), 0)
        
        # Verifica spawns
        self.assertEqual(len(data["player_spawn"]), 2)
        self.assertGreater(len(data["enemy_spawns"]), 0)
        
        # Verifica flags
        self.assertEqual(len(data["flags"]), 10)
    
    def test_all_assets_exist(self):
        """Verifica se todos os assets existem."""
        images_path = os.path.join(src_path, "rallyx_clone", "assets", "images")
        sounds_path = os.path.join(src_path, "rallyx_clone", "assets", "sounds")
        
        # Imagens necessárias
        images = [
            "player_car.png", "enemy_car.png", "flag.png", "smoke.png",
            "icon_life.png", "title.png", "ui_panel.png",
            "tile_road.png", "tile_wall.png", "tile_grass.png", "tile_border.png"
        ]
        
        for img in images:
            path = os.path.join(images_path, img)
            self.assertTrue(os.path.exists(path), f"Missing: {img}")
        
        # Sons necessários
        sounds = [
            "crash.mp3", "engine_loop.mp3", "lose.mp3", "music_loop.mp3",
            "pickup_flag.mp3", "smoke.mp3", "ui_move.mp3", "ui_select.mp3", "win.mp3"
        ]
        
        for snd in sounds:
            path = os.path.join(sounds_path, snd)
            self.assertTrue(os.path.exists(path), f"Missing: {snd}")


if __name__ == "__main__":
    unittest.main()
