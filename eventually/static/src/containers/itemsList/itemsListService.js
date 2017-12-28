const getItemsList = () => {

    return [
        {
            'id': 4,
            'name': 'read book',
            'authors': [12],
            'form': 2,
            'superiors': [2, 4, 12],
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.',
            'estimation': 54000,
            'created_at': 1509539867,
            'updated_at': 1509539867,
        },
        {
            'id': 3,
            'name': 'write tests',
            'authors': [12, 23],
            'form': 1,
            'superiors': [2, 4, 12],
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.',
            'estimation': 54000,
            'created_at': 1509539867,
            'updated_at': 1509539867,
        },
        {
            'id': 2,
            'name': 'complete views',
            'authors': [12],
            'form': 0,
            'superiors': [2, 4, 12],
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem',
            'estimation': 54000,
            'created_at': 1509539867,
            'updated_at': 1509539867,
        }
    ];
};

export default getItemsList;
