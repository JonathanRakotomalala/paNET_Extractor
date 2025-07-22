from src.llm.llm import Llm, QUERY_1, QUERY_2
import json
import pytest

def test_output_format(mocker):
    llm_instance = Llm()
    # mock_pipe = mocker.Mock()
    # mock_pipe.return_value = 
    mocker.patch.object(
        llm_instance, "pipe", new_callable=mocker.PropertyMock, return_value=[
        {
            "generated_text": [
                {"role": "user", "content": " "},
                {
                    "role": "assistant",
                    "content": '{ "techniques": ["small-angle scattering"]}',
                },
            ]
        }
    ]
    )
    

    my_result = llm_instance.llm_run(QUERY_2)

    assert isinstance(json.loads(my_result), dict)


def test_check_first_technics(mocker):
    llm_instance = Llm()
    mock_pipe = mocker.Mock()
    mock_pipe.return_value = [
        {
            "generated_text": [
                {"role": "user", "content": " "},
                {
                    "role": "assistant",
                    "content": '{ "techniques": ["small-angle scattering"]}',
                },
            ]
        }
    ]

    mocker.patch.object(
        Llm, "pipe", new_callable=mocker.PropertyMock, return_value=mock_pipe
    )
    my_result = llm_instance.llm_run(QUERY_1)
    techniques = json.loads(my_result)

    assert techniques["techniques"][0] == "small-angle scattering"


def test_invalid_output_format(mocker):
    llm_instance = Llm()
    mock_pipe = mocker.Mock()
    mock_pipe.return_value = [
        {
            "generated_text": [
                {"role": "user", "content": " "},
                {"role": "assistant", "content": "Hello"},
            ]
        }
    ]

    mocker.patch.object(
        Llm, "pipe", new_callable=mocker.PropertyMock, return_value=mock_pipe
    )
    my_result = llm_instance.llm_run("Hey!")
    with pytest.raises(json.JSONDecodeError):
        json.loads(my_result)
