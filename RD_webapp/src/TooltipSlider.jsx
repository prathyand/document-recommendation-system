import * as React from 'react';
import 'rc-tooltip/assets/bootstrap.css';
import Slider from 'rc-slider';
import raf from 'rc-util/lib/raf';
import Tooltip from 'rc-tooltip';
var __rest = (this && this.__rest) || function (s, e) {
  var t = {};
  for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
      t[p] = s[p];
  if (s != null && typeof Object.getOwnPropertySymbols === "function")
      for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
          if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
              t[p[i]] = s[p[i]];
      }
  return t;
};

const HandleTooltip = (props) => {
  const { value, children, visible, tipFormatter = (val) => `${val}` } = props, restProps = __rest(props, ["value", "children", "visible", "tipFormatter"]);
  const tooltipRef = React.useRef();
  const rafRef = React.useRef(null);
  function cancelKeepAlign() {
      raf.cancel(rafRef.current);
  }
  function keepAlign() {
      rafRef.current = raf(() => {
          var _a;
          (_a = tooltipRef.current) === null || _a === void 0 ? void 0 : _a.forcePopupAlign();
      });
  }
  React.useEffect(() => {
      if (visible) {
          keepAlign();
      }
      else {
          cancelKeepAlign();
      }
      return cancelKeepAlign;
  }, [value, visible]);
  return (React.createElement(Tooltip, Object.assign({ placement: "top", overlay: tipFormatter(value), overlayInnerStyle: { minHeight: 'auto' }, ref: tooltipRef, visible: visible }, restProps), children));
};
export const handleRender = (node, props) => {
  return (React.createElement(HandleTooltip, { value: props.value, visible: props.dragging }, node));
};
const TooltipSlider = (_a) => {
  var { tipFormatter, tipProps } = _a, props = __rest(_a, ["tipFormatter", "tipProps"]);
  const tipHandleRender = (node, handleProps) => {
      return (React.createElement(HandleTooltip, Object.assign({ value: handleProps.value, visible: handleProps.dragging, tipFormatter: tipFormatter }, tipProps), node));
  };
  return React.createElement(Slider, Object.assign({}, props, { handleRender: tipHandleRender }));
};
export default TooltipSlider;