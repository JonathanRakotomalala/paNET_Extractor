from src.llm.llm import Llm,QUERY_1, QUERY_2,DOCUMENT_METADATA_EXTRACTION
import json




def test_output_format(mocker):
    mock_pipe = mocker.Mock()
    mock_pipe.return_value = [
        {
            "generated_text": [
                {
                    "role": "user",
                    "content": " "
                },
                {
                    "role": "assistant",
                    "content": "{ \"techniques\": [\"small-angle scattering\"]}"
                }
            ]
        }
    ]
    my_result  = Llm.llm_run(QUERY_2)
    assert mock_pipe.called_with(DOCUMENT_METADATA_EXTRACTION+QUERY_2)
    assert isinstance(json.loads(my_result),dict)




def test_check_first_technics(mocker):
    mock_pipe = mocker.Mock()
    mock_pipe.return_value = [
        {
            "generated_text": [
                {
                    "role": "user",
                    "content": " "
                },
                {
                    "role": "assistant",
                    "content": "{ \"techniques\": [\"small-angle scattering\"]}"
                }
            ]
        }
    ]

    mocker.patch.object(Llm,'pipe',new_callable= mocker.PropertyMock,return_value=mock_pipe)    
    # mock_pipeline.return_value = mock_pipe
    mocker.patch.object(Llm,'pipe',new_callable= mocker.PropertyMock,return_value=mock_pipe)    
    # mock_pipeline.return_value = mock_pipe
    my_result  = Llm.llm_run(QUERY_1)
    techniques = json.loads(my_result)

    assert mock_pipe.called_with(DOCUMENT_METADATA_EXTRACTION+QUERY_1)
    assert techniques["techniques"][0]== "small-angle scattering"

    # def test_check_french(self):
    #     my_result  = Llm.llm_run(DOCUMENT_METADATA_EXTRACTION,QUERY_3)
    #     techniques = json.loads(my_result)
    #     assert techniques["techniques"][0]== "ICP MS"

    # def test_no_techniques_found(self):
    #     my_result  = Llm.llm_run(DOCUMENT_METADATA_EXTRACTION,"")
    #     assert my_result == []

    def test_invalid_output_format(self):
        mock_pipe = mocker.Mock()
        mock_pipe.return_value = [
            {
                "generated_text": [
                    {
                        "role": "user",
                        "content": " "
                    },
                    {
                        "role": "assistant",
                        "content": "Hello"
                    }
                ]
            }
        ]

        mocker.patch.object(Llm,'pipe',new_callable= mocker.PropertyMock,return_value=mock_pipe)    
        my_result  = Llm.llm_run("",QUERY_2)
        with self.assertRaises(json.JSONDecodeError):
            json.loads(my_result)

    