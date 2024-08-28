import { library, dom } from "@fortawesome/fontawesome-svg-core"
import { faBookmark as fasBookmark, faMagnifyingGlass as fasMagnifyingGlass, faBell as fasBell } from "@fortawesome/free-solid-svg-icons"
import { faBookmark as farBookmark } from "@fortawesome/free-regular-svg-icons"

library.add(farBookmark, fasBookmark, fasMagnifyingGlass, fasBell)
dom.i2svg()