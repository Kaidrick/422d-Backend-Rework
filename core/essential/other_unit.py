import time
import core.utility.data_parsing as parse
import core.data_interface as cdi
import numpy as np


def parse_other_unit(group_id, group_name, coalition, category, unit_data):
    other = OtherUnit(group_id, group_name, coalition, unit_data)
    # print(other.unit_name, other.unit_type, other.unit_pos)
    return other


class OtherUnit:  # AI units and static objects?
    def __init__(self, group_id, group_name, coalition, unit_data):

        # FIXME: consider the need to query the id data of a group added dynamically by script?
        self.runtime_id = unit_data['runtime_id']
        self.runtime_id_name = 'id_' + str(self.runtime_id)

        self.unit_name = unit_data['name']
        self.group_name = group_name

        self.unit_type = unit_data['type']
        self.unit_coalition = coalition  # blue - Enemies, red - ?
        self.unit_country = unit_data['country']

        self.fuel = unit_data['fuel']
        self.velocity = unit_data['velocity']

        self.active_munition = {}  # indexed by weapon runtime id

        # init record field
        self.recent_pos = [unit_data['pos']]  # keep 10 recent position for calculation
        self.recent_pos_time = [time.time()]  # 10 timestamp corresponding to recent position

        # Data to keep updated
        self.last_unit_pos = unit_data['pos']

        self.move_dir = np.array([0, 0, 0])  # moving direction as vec3 in LO

        self.spd_avg = 0

        # Data to keep updated
        self.unit_pos = unit_data['pos']
        self.unit_ll = unit_data['coord']['LL']
        self.unit_att = {  # FIXME
            'pitch': unit_data['att'],
            'bank': unit_data['att'],
            'heading': unit_data['att'],
        }

        self.group_id = group_id

        # data that will be needed but cannot be exported are:
        # velocity?
        # callsign, maybe?
        # fuel
        # north correction
        # ammo

    def update(self, update_data):
        self.last_unit_pos = self.unit_pos

        self.fuel = update_data['fuel']
        self.velocity = update_data['velocity']
        self.unit_pos = update_data['pos']
        self.unit_ll = update_data['coord']['LL']
        self.mgrs = update_data['coord']['MGRS']
        self.unit_att = {  # FIXME
            'pitch': update_data['att'],
            'bank': update_data['att'],
            'heading': update_data['att'],
        }

        # check if player has moved during the last simulation export
        if self.last_unit_pos != self.unit_pos:  # player's position has changed
            array_last_unit_pos = np.array(
                [
                    self.last_unit_pos['x'], self.last_unit_pos['y'], self.last_unit_pos['z']
                ]
            )
            array_unit_pos = np.array(
                [
                    self.unit_pos['x'], self.unit_pos['y'], self.unit_pos['z']
                ]
            )
            self.move_dir = array_unit_pos - array_last_unit_pos

        return self
    # def update(self, update_data):
    #     # record pos data
    #     parse.record_position_time_pair(
    #         update_data['Position'], self.recent_pos, self.recent_pos_time
    #     )
    #
    #     self.unit_pos = update_data['Position']
    #     self.unit_ll = update_data['LatLongAlt']
    #     self.unit_att = {
    #         'pitch': update_data['Pitch'],
    #         'bank': update_data['Bank'],
    #         'heading': update_data['Heading'],
    #     }
