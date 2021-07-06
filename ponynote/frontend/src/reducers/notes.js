const initialState = [
    {text: "Write code!"},
    {text: "Read code!"}
];


export default function mynotes(state=initialState, action) {
    let noteList = state.slice();

    switch (action.type) {

        case 'ADD_NOTE':
            return [...state, {text: action.text}];

        case 'UPDATE_NOTE':
            let noteToUpdate = noteList[action.id]
            noteToUpdate.text = action.text;
            noteList.splice(action.id, 1, noteToUpdate);
            return noteList;

        case 'DELETE_NOTE':
            noteList.splice(action.id, 1);
            return noteList;

        default:
            return state;
    }
}
