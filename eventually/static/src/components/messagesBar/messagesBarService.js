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
        };
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
        };
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
        };
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

export {mentorsService, messagesListService};
