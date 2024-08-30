import { library, dom } from "@fortawesome/fontawesome-svg-core"
import { faBookmark as fasBookmark, faMagnifyingGlass, faBell, faCirclePlus, faBookmark, faMessage, faPlus, faAngleRight, faSortDown, faEllipsis, faShare} from "@fortawesome/free-solid-svg-icons"
import { faBookmark as farBookmark, faComment, faThumbsUp } from "@fortawesome/free-regular-svg-icons"

library.add(farBookmark, fasBookmark, faMagnifyingGlass, faBell, faCirclePlus, faBookmark, faMessage, faPlus, faAngleRight, faSortDown, faEllipsis, faShare, faComment, faThumbsUp)
dom.i2svg()