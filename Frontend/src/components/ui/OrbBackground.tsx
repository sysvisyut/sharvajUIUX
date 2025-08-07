import Orb from './Orb';

const OrbBackground = () => {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden orb-blend">
      {/* Main central orb - single large bubble */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[1200px] h-[1200px]">
        <Orb
          hoverIntensity={0.8}
          rotateOnHover={true}
          hue={240}
          forceHoverState={false}
        />
      </div>
    </div>
  );
};

export default OrbBackground;
