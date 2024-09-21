import { library, dom } from "@fortawesome/fontawesome-svg-core"
import { faBookmark as fasBookmark, faMagnifyingGlass, faBell, faCirclePlus, faBookmark, faMessage, faPlus, faAngleRight, faSortDown, faSortUp, faEllipsis, faShare, faXmark, faP, faCircle, faMoneyBillTrendUp, faCommentDots, faChartLine, faUser, faList } from "@fortawesome/free-solid-svg-icons"
import { faBookmark as farBookmark, faComment, faThumbsUp, faList as farList } from "@fortawesome/free-regular-svg-icons"
import Alpine from "alpinejs"

library.add(farBookmark, fasBookmark, faMagnifyingGlass, faBell, faCirclePlus, faBookmark, faMessage, faPlus, faAngleRight, faSortDown, faSortUp, faEllipsis, faShare, faComment, faThumbsUp, faXmark, faP, faCircle, faMoneyBillTrendUp, faCommentDots, faChartLine, faUser, faList, farList)
dom.i2svg()

document.addEventListener("htmx:afterRequest", () => {
    dom.i2svg();
});

Alpine.data("like_icon", () => ({
    init() {
        dom.i2svg();
    }
}));
