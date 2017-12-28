const getReceiversList = (isMentor=false) => {

    let receivers = {};

    if (isMentor) {

        receivers = {
            'receivers': [
                {
                    'id': 1,
                    'first_name': 'Sam',
                    'last_name': 'Ruby',
                    'avatar': 'samruby',
                    'is_online': true
                },
                {
                    'id': 2,
                    'first_name': 'Marcelo',
                    'last_name': 'Petrov',
                    'avatar': 'marcelopetrov',
                    'is_online': false
                },
                {
                    'id': 3,
                    'first_name': 'Ismail',
                    'last_name': 'Botobo',
                    'avatar': 'ismailbotobo',
                    'is_online': true
                }
            ]
        };

    } else {

        receivers = {
            'receivers': [
                {
                    'id': 1,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'avatar': 'johndoe',
                    'is_online': true
                },
                {
                    'id': 2,
                    'first_name': 'Eric',
                    'last_name': 'Moreno',
                    'avatar': 'ericmoreno',
                    'is_online': false
                },
                {
                    'id': 3,
                    'first_name': 'Mark',
                    'last_name': 'Smith',
                    'avatar': 'marksmith',
                    'is_online': true
                }
            ]
        };
    }

    return receivers;
};

const getMessagesList = receiverId => {
    let messages = null;

    if (receiverId === 1) {
        messages = {
            'messages': [
                {
                    'id': 1,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'created_at': 1514412290374,
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                },
                {
                    'id': 2,
                    'author': 'Me',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
                },
                {
                    'id': 3,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 4,
                    'author': 'Me',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 5,
                    'author': 'Me',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 6,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                }
            ]
        };
    } else if (receiverId === 2) {
        messages = {
            'messages': [
                {
                    'id': 1,
                    'author': 'Eric Moreno',
                    'avatar': 'ericmoreno',
                    'created_at': 1514412290374,
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 2,
                    'author': 'Me',
                    'created_at': 1514412290374,
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
                },
                {
                    'id': 3,
                    'author': 'Eric Moreno',
                    'avatar': 'ericmoreno',
                    'created_at': 1514412290374,
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla'
                },
                {
                    'id': 4,
                    'author': 'Me',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 5,
                    'author': 'Me',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 6,
                    'avatar': 'ericmoreno',
                    'author': 'Eric Moreno',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                }
            ]
        };
    } else if (receiverId === 3) {
        messages = {
            'messages': [
                {
                    'id': 1,
                    'author': 'Mark Smith',
                    'avatar': 'marksmith',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
                },
                {
                    'id': 2,
                    'author': 'Me',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 3,
                    'author': 'Mark Smith',
                    'avatar': 'marksmith',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 4,
                    'author': 'Me',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 5,
                    'author': 'Me',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 6,
                    'author': 'Mark Smith',
                    'avatar': 'marksmith',
                    'created_at': 1514412290374,                    
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                }
            ]
        };
    }

    return messages;
};

export {getReceiversList, getMessagesList};
