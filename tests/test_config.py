from philomas_pipeline.config import load_animations


def test_load_animations_reads_data_driven_timing_and_loop_flags():
    animations = load_animations()

    assert animations["idle"]["frames"] == 6
    assert animations["idle"]["loop"] is True
    assert animations["idle"]["frame_duration_ms"] == 120
    assert animations["death"]["frames"] == 8
    assert animations["death"]["loop"] is False
    assert animations["death"]["frame_duration_ms"] == 140
