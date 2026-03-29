from hm_scraper.pipelines import SaveToRDBMSPipeline


def test_pipeline_open_spider_success(mock_db_service, mock_spider):
    mock_db_service.connect.return_value = True
    mock_db_service.create_or_replace_products_table.return_value = True

    pipeline = SaveToRDBMSPipeline()
    pipeline.open_spider(mock_spider)

    assert mock_db_service.connect.called
    assert mock_db_service.create_or_replace_products_table.called
    assert "Database connection successful" in mock_spider.logger.info.call_args[0][0]


def test_pipeline_open_spider_failure(mock_db_service, mock_spider):
    mock_db_service.connect.return_value = False

    pipeline = SaveToRDBMSPipeline()
    pipeline.open_spider(mock_spider)

    assert mock_db_service.connect.called
    assert (
        "Failed to initialize database connection"
        in mock_spider.logger.error.call_args[0][0]
    )


def test_pipeline_process_item_success(mock_db_service, mock_item, mock_spider):
    mock_db_service.save_product.return_value = True

    pipeline = SaveToRDBMSPipeline()
    result = pipeline.process_item(mock_item, mock_spider)

    assert result == mock_item
    mock_db_service.save_product.assert_called_once_with(mock_item)
    assert "Saving to DB successful" in mock_spider.logger.info.call_args[0][0]


def test_pipeline_process_item_failure(mock_db_service, mock_item, mock_spider):
    mock_db_service.save_product.return_value = False

    pipeline = SaveToRDBMSPipeline()
    result = pipeline.process_item(mock_item, mock_spider)

    assert result == mock_item
    assert "Error saving to DB" in mock_spider.logger.error.call_args[0][0]


def test_pipeline_close_spider(mock_db_service):
    pipeline = SaveToRDBMSPipeline()
    pipeline.close_spider()

    assert mock_db_service.close.called
