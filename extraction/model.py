import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class RawDataInfo:
    machine_model: str
    city_code: int
    election_zone_code: int
    election_section_code: int
    election_local_code: int
    source_file_name: str

    def __eq__(self, o: object) -> bool:
        return self.machine_model == o.machine_model \
               and self.city_code == o.city_code \
               and self.election_zone_code == o.election_zone_code \
               and self.election_section_code == o.election_section_code \
               and self.election_local_code == o.election_local_code \
               and self.source_file_name == o.source_file_name
