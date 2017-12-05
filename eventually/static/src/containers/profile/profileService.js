const itemsListService = () => {
    const items = {
        'items': [
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
        ]
    };

    return items;
};

const messagesListService = id => {
    let messages = null;

    if (id == 1) {
        messages = {
            'messages': [
                {
                    'id': 1,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                },
                {
                    'id': 2,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
                },
                {
                    'id': 3,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 4,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 5,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 6,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                }
            ]
        }
    } else if (id == 2) {
        messages = {
            'messages': [
                {
                    'id': 1,
                    'author': 'Eric Moreno',
                    'avatar': 'ericmoreno',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 2,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
                },
                {
                    'id': 3,
                    'author': 'Eric Moreno',
                    'avatar': 'ericmoreno',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla'
                },
                {
                    'id': 4,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 5,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 6,
                    'avatar': 'ericmoreno',
                    'author': 'Eric Moreno',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                }
            ]
        }
    } else if (id == 3) {
        messages = {
            'messages': [
                {
                    'id': 1,
                    'author': 'Mark Smith',
                    'avatar': 'marksmith',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
                },
                {
                    'id': 2,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 3,
                    'author': 'Mark Smith',
                    'avatar': 'marksmith',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 4,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 5,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 6,
                    'author': 'Mark Smith',
                    'avatar': 'marksmith',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                }
            ]
        }
    }

    return messages;
};

const mentorsService = () => {
    let mentors = {
        'mentors': [
            {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
                'avatar': 'johndoe'
            },
            {
                'id': 2,
                'first_name': 'Eric',
                'last_name': 'Moreno',
                'avatar': 'ericmoreno'
            },
            {
                'id': 3,
                'first_name': 'Mark',
                'last_name': 'Smith',
                'avatar': 'marksmith'
            }
        ]
    };

    return mentors;
};

export {itemsListService, messagesListService, mentorsService}
