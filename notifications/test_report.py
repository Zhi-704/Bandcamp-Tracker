'''Testing suite for report.py'''

from unittest.mock import patch, MagicMock
import pytest
from report import (
    filter_topics,
    get_sales_data_of_tag,
    extract_tag_name,
    publish_list_to_topic,
    add_tags_to_dictionary,
    get_trending_items
)


topic_list = [
    {"TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic"},
    {"TopicArn": "arn:aws:sns:us-east-1:123456789012:AnotherTopic"},
    {"TopicArn": "arn:aws:sns:us-east-1:123456789012:YetAnotherTopic"},
    {"TopicArn": "arn:aws:sns:us-west-2:123456789012:ExampleTopic"},
]


@pytest.mark.parametrize("filter_word, expected_topics", [
    ("us-east-1", [
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic"},
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:AnotherTopic"},
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:YetAnotherTopic"},
    ]),
    ("ExampleTopic", [
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic"},
        {"TopicArn": "arn:aws:sns:us-west-2:123456789012:ExampleTopic"},
    ]),
    ("us-west-2", [
        {"TopicArn": "arn:aws:sns:us-west-2:123456789012:ExampleTopic"},
    ]),
    ("random", []),
    ("123456789012", [
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic"},
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:AnotherTopic"},
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:YetAnotherTopic"},
        {"TopicArn": "arn:aws:sns:us-west-2:123456789012:ExampleTopic"},
    ]),
    ("", topic_list)
])
def test_filter_topics(filter_word, expected_topics):
    '''Test base cases for filter topics'''
    filtered_topics = [topic['TopicArn']
                       for topic in filter_topics(filter_word, topic_list)]
    expected_topic_arns = [topic['TopicArn'] for topic in expected_topics]
    assert filtered_topics == expected_topic_arns

    assert len(filtered_topics) == len(expected_topic_arns)


@pytest.mark.parametrize("topic_arn, expected_tag_name", [
    ("arn:aws:sns:us-east-1:123456789012:ExampleTopic-beach-Spongebob-remix-trap",
     "Spongebob remix trap"),
    ("arn:aws:sns:us-east-1:123456789012:ExampleTopic-abc-biggie-littley", "biggie littley"),
    ("arn:aws:sns:us-east-1:123456789012:AnotherTopic-123-456-789", "456 789"),
    ("arn:aws:sns:us-west-2:123456789012:YetAnotherTopic-xyz-abc-123-i-dont-know-how-to-read",
     "abc 123 i dont know how to read"),
    ("arn:aws:sns:us-east-1:123456789012:ExampleTopic-1-2-3", "2 3"),
])
def test_extract_tag_name(topic_arn, expected_tag_name):
    '''Base cases for extract tag name'''
    assert extract_tag_name(topic_arn) == expected_tag_name


@pytest.mark.parametrize("topic_arn, expected_tag_name", [
    ("arn:aws:sns:us-west-1:123456789012:ExampleTopic", ""),
    ("", ""),
    (None, None),
    ([1, 2], None),
    (['str'], None),
    ("invalid_arn_format", "")
])
def test_extract_tag_name_edge_cases(topic_arn, expected_tag_name):
    '''Testing edge cases such as empty for extract tag name'''
    assert extract_tag_name(topic_arn) == expected_tag_name


@pytest.mark.parametrize("tags_list, expected_tags_list", [
    ([
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic-abc-def-ghi"},
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:AnotherTopic-sponge-bob-pants"},
        {"TopicArn": "arn:aws:sns:us-west-2:123456789012:YetAnotherTopic-xyz-how-do-i-read"},
    ], [
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic-abc-def-ghi",
            "Tag": "def ghi"},
        {"TopicArn": "arn:aws:sns:us-east-1:123456789012:AnotherTopic-sponge-bob-pants",
            "Tag": "bob pants"},
        {"TopicArn": "arn:aws:sns:us-west-2:123456789012:YetAnotherTopic-xyz-how-do-i-read",
            "Tag": "how do i read"},
    ]),
    ([], []),
    ([
        {"TopicArn": "arn:aws:sns:us-west-1:123456789012:truncated"},
        {"TopicArn": ""},
        {"TopicArn": "invalid_arn_format"},
    ], [
        {"TopicArn": "arn:aws:sns:us-west-1:123456789012:truncated", "Tag": ""},
        {"TopicArn": "", "Tag": ""},
        {"TopicArn": "invalid_arn_format", "Tag": ""},
    ])
])
def test_add_tags_to_dictionary(tags_list, expected_tags_list):
    '''Tests for both base case and edge case for add_tag_to_dictionary'''
    assert add_tags_to_dictionary(tags_list) == expected_tags_list


@patch('report.get_sales_data_of_tag')
def test_get_trending_items(mock_get_sales):
    '''Test get trending items if key is inserted correctly'''
    mock_get_sales.return_value = [
        {"name": "Item1", "sales": 100},
        {"name": "Item2", "sales": 150},
        {"name": "Item3", "sales": 200}
    ]

    mock_connection = MagicMock()

    trending_items = get_trending_items(
        mock_connection, "placeholder_type", "placeholder_tag")

    assert len(trending_items) == 3
    assert all('type' in item for item in trending_items)

    mock_get_sales.assert_called_once_with(
        mock_connection, "placeholder_type", "placeholder_tag")


class TestPublishListToTopic():
    '''Class for testing get_sales_data_of_tag. Contains all base case and edge cases tests'''

    def test_publish_list_to_topic_base(self):
        '''Tests base case where it sends emails to subscribed users'''
        mock_sns_client = MagicMock()
        topic_arn = "arn:aws:sns:us-west-2:123456789012:ExampleTopic"
        tag = "spongebob trap house"
        trending_data = [
            {"title": "Track1", "band": "Artist1", "type": "track",
                "url": "https://example.com/track1"},
            {"title": "Album2", "band": "Artist2", "type": "album",
                "url": "https://example.com/album2"}
        ]

        publish_list_to_topic(
            mock_sns_client, topic_arn, tag, trending_data)

        mock_sns_client.publish.assert_called_once_with(
            TopicArn=topic_arn,
            Subject=f"What's trending for {tag}?",
            Message='''These items are trending for the tag spongebob trap house!\n\nTrack 'Track1' by 'Artist1' is currently trending!\nCheck it out here at: https://example.com/track1\n\nAlbum 'Album2' by 'Artist2' is currently trending!\nCheck it out here at: https://example.com/album2\n\n'''
        )

        published_message = mock_sns_client.publish.call_args.kwargs['Message']
        assert "These items are trending for the tag spongebob trap house!" in published_message
        assert "Track 'Track1' by 'Artist1' is currently trending!" in published_message
        assert "Album 'Album2' by 'Artist2' is currently trending!" in published_message

    def test_publish_list_to_topic_missing_keys(self):
        'Tests for case where the items are missing keys'
        mock_sns_client = MagicMock()
        topic_arn = "arn:aws:sns:us-west-2:123456789012:ExampleTopic"
        tag = "spongebob trap house"
        trending_data = [
            {"title": "Track1", "band": "Artist1", "type": "track",
                "url": "https://example.com/track1"},
            {"title": "Album2", "band": "Artist2", "type": "album",
                "url": "https://example.com/album2"},
            {"title": "qwerty", "band": "Artist3",
                "type": "track"},
            {"title": "lord_of_the_rings", "band": "Artist4",
                "url": "wagwan"}
        ]

        publish_list_to_topic(mock_sns_client, topic_arn, tag, trending_data)

        published_message = mock_sns_client.publish.call_args.kwargs['Message']
        assert "These items are trending for the tag spongebob trap house!" in published_message
        assert "Track 'Track1' by 'Artist1' is currently trending!" in published_message
        assert "Album 'Album2' by 'Artist2' is currently trending!" in published_message
        assert "wagwan" not in published_message
        assert "lord_of_the_rings" not in published_message
        assert "qwerty" not in published_message


class TestGetSalesDataOfTag():
    '''Class for testing get_sales_data_of_tag. Contains all base case and edge cases tests'''

    def test_get_sales_data_of_tag_success(self):
        '''Test base case for getting sales'''

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"track_id": 1, "title": "Hottake", "band": "Author1",
                "copies_sold": 120, "url": "https://example.com/dsadsa"},
            {"track_id": 2, "title": "Mixtake", "band": "Author2",
                "copies_sold": 110, "url": "https://example.com/dafdsf"}
        ]
        mock_cursor.__enter__.return_value = mock_cursor
        mock_connection.cursor.return_value = mock_cursor

        trending_items = get_sales_data_of_tag(
            mock_connection, "placeholder_type", "placeholder_tag")

        assert len(trending_items) == 2
        assert "track_id" in trending_items[0]
        assert "copies_sold" in trending_items[0]
        assert trending_items[0]["copies_sold"] == 120

    def test_get_sales_data_of_tag_exception_handling(self):
        '''Tests in case when exception occurs'''
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception(
            "Database connection error")
        mock_cursor.__enter__.return_value = mock_cursor
        mock_connection.cursor.return_value = mock_cursor

        trending_items = get_sales_data_of_tag(
            mock_connection, "placeholder_type", "placeholder_tag")

        assert len(trending_items) == 0
        assert mock_connection.rollback.call_count == 1

    def test_get_sales_data_of_tag_no_data(self):
        '''Tests for case when no data is retrieved'''
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_cursor.__enter__.return_value = mock_cursor
        mock_connection.cursor.return_value = mock_cursor

        trending_items_empty = get_sales_data_of_tag(
            mock_connection, "placeholder_type", "placeholder_tag")
        assert trending_items_empty == []
