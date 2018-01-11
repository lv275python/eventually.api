const getMessagesSet = (messagesList) => {
    let uniqueMessages = {};
    messagesList.forEach(message => {
        uniqueMessages[message.created_at] = message;
    });
    return Object.values(uniqueMessages).reverse();
};

const getNextPageNumber = (messagesList, defaultPage, messagesPerPage) => {
    return Math.floor(messagesList.length / messagesPerPage) + defaultPage;
};

export { getMessagesSet, getNextPageNumber };
