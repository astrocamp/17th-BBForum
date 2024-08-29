import { library, dom } from "@fortawesome/fontawesome-svg-core"
import { faBookmark as fasBookmark, faMagnifyingGlass, faBell, faCirclePlus, faBookmark, faMessage} from "@fortawesome/free-solid-svg-icons"
import { faBookmark as farBookmark } from "@fortawesome/free-regular-svg-icons"

library.add(farBookmark, fasBookmark, faMagnifyingGlass, faBell, faCirclePlus, faBookmark, faMessage)
dom.i2svg()