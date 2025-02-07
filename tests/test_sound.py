from unittest import TestCase
from unittest.mock import MagicMock, patch

import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.game_sound import Sound




# This is a test class for the Sound class in /data/game_sound.py.
# This class handles all sound for the game.
# There is at least one test for each Sound method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestSound(TestCase):

    def setUp(self):
        self.music_dict = {'death': 'death.wav', 'out_of_time': 'out_of_time.wav', 'invincible': 'invincible.ogg',
                           'world_clear': 'world_clear.wav', 'main_theme': 'main_theme.ogg', 'flagpole': 'flagpole.wav',
                           'main_theme_sped_up': 'main_theme_sped_up.ogg', 'stage_clear': 'stage_clear.wav',
                           'game_over': 'game_over.ogg'}

        self.overhead_info = MagicMock()
        self.overhead_info.state = c.LEVEL
        self.overhead_info.game_info = {}
        with patch('SuperMarioLevel1.data.setup.SFX', {'sound_effect': MagicMock()}), patch(
                'SuperMarioLevel1.data.setup.MUSIC', self.music_dict), patch('pygame.mixer.music.load'), patch(
            'pygame.mixer.music.play'):
            self.sound = Sound(self.overhead_info)

    def test_init(self):
        self.assertIsNotNone(self.sound.sfx_dict)
        self.assertIsNotNone(self.sound.music_dict)
        self.assertEqual(self.sound.overhead_info, self.overhead_info)
        self.assertEqual(self.sound.game_info, self.overhead_info.game_info)
        self.assertEqual(self.sound.state, c.NORMAL)

    def test_set_music_mixer(self):
        with patch('pygame.mixer.music.load') as mock_load, patch('pygame.mixer.music.play') as mock_play:
            # Test when overhead_info.state is LEVEL
            self.overhead_info.state = c.LEVEL
            self.sound.set_music_mixer()
            mock_load.assert_called_once_with(self.sound.music_dict['main_theme'])
            mock_play.assert_called_once_with()
            self.assertEqual(self.sound.state, c.NORMAL)

            # Reset mock calls
            mock_load.reset_mock()
            mock_play.reset_mock()

            # Test when overhead_info.state is GAME_OVER
            self.overhead_info.state = c.GAME_OVER
            self.sound.set_music_mixer()
            mock_load.assert_called_once_with(self.sound.music_dict['game_over'])
            mock_play.assert_called_once_with()
            self.assertEqual(self.sound.state, c.GAME_OVER)

    def test_update(self):
        mario = MagicMock()
        mario.dead = False
        mario.invincible = False
        mario.losing_invincibility = False
        mario.state = c.WALK
        self.sound.state = c.NORMAL
        with patch('pygame.mixer.music.get_busy', return_value=0), patch('pygame.mixer.music.load'), patch(
                'pygame.mixer.music.play'):
            self.sound.update({'test_key': 'test_value'}, mario)
            self.assertEqual(self.sound.game_info, {'test_key': 'test_value'})
            self.assertEqual(self.sound.mario, mario)

    def test_play_music(self):
        with patch('pygame.mixer.music.load'), patch('pygame.mixer.music.play'):
            self.sound.play_music('main_theme', c.FLAGPOLE)
            self.assertEqual(self.sound.state, c.FLAGPOLE)

    def test_stop_music(self):
        with patch('pygame.mixer.music.stop'):
            self.sound.stop_music()

    def test_handle_state_normal_dead(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.sound.state = c.NORMAL
        self.mario.dead = True
        with patch.object(self.sound, 'play_music') as play_music_mock:
            self.sound.update({}, self.mario)
            play_music_mock.assert_called_once_with('death', c.MARIO_DEAD)

    def test_handle_state_normal_invincible(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.sound.state = c.NORMAL
        self.mario.dead = False
        self.mario.invincible = True
        self.mario.losing_invincibility = False
        with patch.object(self.sound, 'play_music') as play_music_mock:
            self.sound.update({}, self.mario)
            play_music_mock.assert_called_once_with('invincible', c.MARIO_INVINCIBLE)

    def test_handle_state_normal_flagpole(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.sound.state = c.NORMAL
        self.mario.dead = False
        self.mario.invincible = False
        self.mario.state = c.FLAGPOLE
        with patch.object(self.sound, 'play_music') as play_music_mock:
            self.sound.update({}, self.mario)
            play_music_mock.assert_called_once_with('flagpole', c.FLAGPOLE)

    # def test_handle_state_normal_time_warning(self):
    #     self.overhead_info = MagicMock()
    #     self.sound = Sound(self.overhead_info)
    #     self.mario = MagicMock()
    #     self.sound.state = c.NORMAL
    #     self.mario.dead = False
    #     self.mario.invincible = False
    #     self.mario.state = c.STAND
    #     self.overhead_info.time = 100
    #     self.sound.update({}, self.mario)
    #     with patch.object(self.sound, 'play_music') as play_music_mock:
    #         self.sound.update({}, self.mario)
    #         play_music_mock.assert_called_once_with('out_of_time', c.TIME_WARNING)

    def test_handle_state_flagpole_walking_to_castle(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.sound.state = c.FLAGPOLE
        self.mario.state = c.WALKING_TO_CASTLE
        with patch.object(self.sound, 'play_music') as play_music_mock:
            self.sound.update({}, self.mario)
            play_music_mock.assert_called_once_with('stage_clear', c.STAGE_CLEAR)

    #
    # def test_handle_state_stage_clear_in_castle(self):
    #     self.overhead_info = MagicMock()
    #     self.sound = Sound(self.overhead_info)
    #     self.mario = MagicMock()
    #     self.sound.state = c.STAGE_CLEAR
    #     self.mario.in_castle = True
    #     with patch.object(self.sound.sfx_dict['count_down'], 'play') as play_mock:
    #         self.sound.update({}, self.mario)
    #         play_mock.assert_called_once()
    #         self.assertEqual(self.sound.state, c.FAST_COUNT_DOWN)

    def test_handle_state_normal_flagpole_1(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.sound.state = c.NORMAL
        self.mario.dead = False
        self.mario.invincible = False
        self.mario.state = c.FLAGPOLE
        with patch.object(self.sound, 'play_music') as play_music_mock:
            self.sound.update({}, self.mario)
            play_music_mock.assert_called_once_with('flagpole', c.FLAGPOLE)

    def test_handle_state_normal_time_warning(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.sound.state = c.NORMAL
        self.mario.dead = False
        self.mario.invincible = False
        self.mario.state = c.STAND
        self.overhead_info.time = 100
        with patch.object(self.sound, 'play_music') as play_music_mock:
            self.sound.update({}, self.mario)
            play_music_mock.assert_called_once_with('out_of_time', c.TIME_WARNING)

    def test_handle_state_flagpole_walking_to_castle(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.sound.state = c.FLAGPOLE
        self.mario.state = c.WALKING_TO_CASTLE
        with patch.object(self.sound, 'play_music') as play_music_mock:
            self.sound.update({}, self.mario)
            play_music_mock.assert_called_once_with('stage_clear', c.STAGE_CLEAR)

    def test_handle_state_stage_clear(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.mario.in_castle = True
        self.sound.state = c.STAGE_CLEAR
        self.mario.state = c.WALKING_TO_CASTLE
        self.sound.sfx_dict['count_down'] = MagicMock()
        with patch.object(self.sound.sfx_dict['count_down'], 'play') as mock_play:
            self.sound.update({}, self.mario)
            self.sound.handle_state()
            self.assertEqual(self.sound.state, c.FAST_COUNT_DOWN)
            mock_play.assert_called_once_with()

    def test_handle_state_fast_count_down(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.mario.in_castle = True
        self.sound.state = c.FAST_COUNT_DOWN
        self.sound.overhead_info.time = 0
        self.sound.sfx_dict['count_down'] = MagicMock()
        with patch.object(self.sound.sfx_dict['count_down'], 'stop') as mock_stop:
            self.sound.update({}, self.mario)
            self.sound.handle_state()
            self.assertEqual(self.sound.state, c.WORLD_CLEAR)
            mock_stop.assert_called_once_with()

    def test_handle_state_time_warning_case_1(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.mario.in_castle = True
        self.sound.state = c.TIME_WARNING
        self.sound.overhead_info.time = 0
        self.sound.sfx_dict['count_down'] = MagicMock()
        with patch.object(self.sound, 'play_music') as mock_play_music, \
                patch('pygame.mixer.music.get_busy', return_value=0):
            self.sound.update({}, self.mario)
            self.sound.handle_state()
            mock_play_music.assert_called_with('main_theme_sped_up', c.SPED_UP_NORMAL)

    def test_handle_state_time_warning_case_2(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.mario.in_castle = True
        self.mario.dead = True
        self.sound.state = c.TIME_WARNING
        self.sound.overhead_info.time = 0
        self.sound.sfx_dict['count_down'] = MagicMock()
        with patch.object(self.sound, 'play_music') as mock_play_music, \
                patch('pygame.mixer.music.get_busy', return_value=1):
            self.sound.update({}, self.mario)
            self.sound.handle_state()
            mock_play_music.assert_called_with('death', c.MARIO_DEAD)

    def test_handle_state_sped_up_normal_case_1(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.mario.in_castle = True
        self.mario.dead = True
        self.sound.state = c.SPED_UP_NORMAL
        self.sound.overhead_info.time = 0
        self.sound.sfx_dict['count_down'] = MagicMock()
        with patch.object(self.sound, 'play_music') as mock_play_music, \
                patch('pygame.mixer.music.get_busy', return_value=1):
            self.sound.update({}, self.mario)
            self.sound.handle_state()
            mock_play_music.assert_called_with('death', c.MARIO_DEAD)

    def test_handle_state_sped_up_normal_case_2(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.mario.in_castle = True
        self.mario.dead = False
        self.mario.state = c.FLAGPOLE
        self.sound.state = c.SPED_UP_NORMAL
        self.sound.overhead_info.time = 0
        self.sound.sfx_dict['count_down'] = MagicMock()
        with patch.object(self.sound, 'play_music') as mock_play_music, \
                patch('pygame.mixer.music.get_busy', return_value=1):
            self.sound.update({}, self.mario)
            self.sound.handle_state()
            mock_play_music.assert_called_with('flagpole', c.FLAGPOLE)

    def test_handle_state_mario_invincible_case_1(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.mario.in_castle = True
        self.mario.dead = False
        self.mario.state = c.FLAGPOLE
        self.mario.current_time = 100000000
        self.mario.invincible_start_timer = 0
        self.sound.state = c.MARIO_INVINCIBLE
        self.sound.overhead_info.time = 0
        self.sound.sfx_dict['count_down'] = MagicMock()
        with patch.object(self.sound, 'play_music') as mock_play_music, \
                patch('pygame.mixer.music.get_busy', return_value=1):
            self.sound.update({}, self.mario)
            self.sound.handle_state()
            mock_play_music.assert_called_with('main_theme', c.NORMAL)

    def test_handle_state_mario_invincible_case_2(self):
        self.overhead_info = MagicMock()
        self.sound = Sound(self.overhead_info)
        self.mario = MagicMock()
        self.mario.in_castle = True
        self.mario.dead = True
        self.mario.state = c.FLAGPOLE
        self.mario.current_time = 1
        self.mario.invincible_start_timer = 1
        self.sound.state = c.MARIO_INVINCIBLE
        self.sound.overhead_info.time = 0
        self.sound.sfx_dict['count_down'] = MagicMock()
        with patch.object(self.sound, 'play_music') as mock_play_music, \
                patch('pygame.mixer.music.get_busy', return_value=1):
            self.sound.update({}, self.mario)
            self.sound.handle_state()
            mock_play_music.assert_called_with('death', c.MARIO_DEAD)

    def test_handle_state_world_clear(self):
        self.sound.state = c.WORLD_CLEAR
        self.sound.handle_state()

    def test_handle_state_mario_dead(self):
        self.sound.state = c.MARIO_DEAD
        self.sound.handle_state()

    def test_handle_state_game_over(self):
        self.sound.state = c.GAME_OVER
        self.sound.handle_state()
