import CurriculumDialog from './curriculum/CurriculumDialog';
import CurriculumLink from './curriculum/CurriculumLink';
import CurriculumList from './curriculum/CurriculumList';
import {
    getCurriculums,
    getTopicListService} from './curriculum/CurriculumService';
import FileHandler from './fileUpload/fileUpload';
import imageValidator from './fileUpload/fileUploadHelper';
import sendFile from './fileUpload/fileUploadService';
import Answer from './item/Answer';
import Assignment from './item/Assignment';
import Item from './item/Item';
import {getData, sendAnswer} from './item/ItemService';
import Literature from './item/Literature';
import TimeLeft from './item/TimeLeft';
import ItemsList from './itemList/ItemsList';
import getItemsList from './itemList/itemsListService';
import ItemUnit from './itemList/ItemUnit';
import AnswerInfo from './mentorItem/AnswerInfo';
import AssignmentInfo from './mentorItem/AssignmentInfo';
import MentorItem from './mentorItem/MentorItem';
import {
    messagesListService,
    studentService,
    itemInfoService,
    answerInfoService} from './mentorItem/MentorItemService';
import MentorMessagesItem from './mentorItem/MessageItem';
import MentorMessagesBar from './mentorItem/MessagesBar';
import MentorMessagesList from './mentorItem/MessagesList';
import MentorMessagesSender from './mentorItem/MessagesSender';
import SetGrade from './mentorItem/SetGrade';
import TmpMentorItem from './mentorItem/tmpStudentItem';
import MentorDashboard from './mentorDashboard/MentorDashboard';
import MessagesItem from './messagesBar/MessageItem';
import MessagesBar from './messagesBar/MessagesBar';
import {
    getMessagesSet,
    getNextPageNumber} from './messagesBar/MessagesBarHelper';
import {
    getMessagesList,
    postChatMessage,
    getOnlineUsers,
    getMentorsListService,
    getStudentsListService} from './messagesBar/MessagesBarService';
import MessagesList from './messagesBar/MessagesList';
import MessagesSender from './messagesBar/MessagesSender';
import ReceiverItem from './messagesBar/ReceiverItem';
import ReceiversList from './messagesBar/ReceiversList';
import Profile from './profile/Profile';
import ProfileEdit from './profile/ProfileEdit';
import {
    putProfileService,
    getProfileService} from './profile/ProfileServices';
import ProfileView from './profile/ProfileView';
import ProgressGraph from './progressGraph/ProgressGraph';
import Forget from './registerLogin/Forget';
import Login from './registerLogin/Login';
import Logout from './registerLogin/Logout';
import Register from './registerLogin/Register';
import {
    loginService,
    forgetPasswordService,
    registerService,
    logoutService} from './registerLogin/registrationService';
import Sign from './registerLogin/Sign';
import CreateTeamDialog from './teamList/CreateTeamDialog';
import EditTeamDialog from './teamList/EditTeamDialog';
import TeamItem from './teamList/TeamItem';
import TeamList from './teamList/TeamList';
import {
    teamServiceGet,
    teamServicePut,
    teamServiceGetMembers,
    teamServicePost,
    usersServiceGet} from './teamList/TeamService';
import TopicDialog from './topicList/TopicDialog';
import TopicItem from './topicList/TopicItem';
import TopicsList from './topicList/TopicsList';
import ProgressProfile from './userProgress/UserProgress';
import Home from './Home';
