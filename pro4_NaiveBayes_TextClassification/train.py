import models

if __name__ == '__main__':
    train_data = models.Prepare("train")
    test_data = models.Prepare("test")

    train_data.create_dic()
    test_data.create_dic()

    train_data.count_tokens()
    test_data.count_tokens()

    train_data.create_news_group()
    test_data.create_news_group()

    print("开始训练...")
    model = models.NaiveBayes(train_data.Count_Path)
    model.nb_multinomial_train(train_data.news_group)
    print("开始预测...")
    model.nb_multinomial_test(test_data.news_group)
    print("运行成功！")
