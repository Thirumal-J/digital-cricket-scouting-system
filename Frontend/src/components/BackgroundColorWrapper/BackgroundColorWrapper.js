import {
  BackgroundColorContext,
  backgroundColors
} from "contexts/BackgroundColorContext";
import { useState } from "react";

export default function BackgroundColorWrapper(props) {
  const [color, setColor] = useState(backgroundColors.blue);

  function changeColor(color) {
    setColor(color);
  }

  return (
    <BackgroundColorContext.Provider
      value={{ color: color, changeColor: changeColor }}
    >
      {props.children}
    </BackgroundColorContext.Provider>
  );
}
