import BattingEvaluator from "views/BattingEvaluator.js";
import BowlingEvaluator from "views/BowlingEvaluator.js";
import Home from "views/Home.js";
import HowAppWorks from "views/HowAppWorks.js";
import ScoutBatsman from "views/ScoutBatsman.js";
import ScoutBowler from "views/ScoutBowler.js";


var routes = [
  {
    path: "/home",
    name: "Home",
    icon: "tim-icons icon-bank",
    component: Home,
    layout: "/admin",
  },
  {
    path: "/scoutBatsman",
    name: "Scout Batsman",
    icon: "tim-icons icon-controller",
    component: ScoutBatsman,
    layout: "/admin",
  },
  {
    path: "/scoutBowler",
    name: "Scout Bowler",
    icon: "tim-icons icon-controller",
    component: ScoutBowler,
    layout: "/admin",
  },
  {
    path: "/predictBattingPerformance",
    name: "Batting Evaluator",
    icon: "tim-icons icon-sound-wave",
    component: BattingEvaluator,
    layout: "/admin",
  },
  {
    path: "/predictBowlingPerformance",
    name: "Bowling Evaluator",
    icon: "tim-icons icon-sound-wave",
    component: BowlingEvaluator,
    layout: "/admin",
  },
  {
    path: "/howAppWorks",
    name: "How App Works",
    icon: "tim-icons icon-sound-wave",
    component: HowAppWorks,
    layout: "/admin",
  }
];
export default routes;
