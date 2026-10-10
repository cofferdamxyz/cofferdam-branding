/* Cofferdam web renditions — window.Cofferdam. Types are documentation. */
import type * as React from 'react';

export interface ButtonProps {
  /** Visible label; also the accessible name unless accessibilityLabel is set. */
  label: string;
  onPress?: () => void;
  /** primary = solid fg on bg · secondary = border outline · ghost = fg-muted text. Default primary. */
  variant?: 'primary' | 'secondary' | 'ghost';
  /** lg = 56px · md = 44px. Default lg. */
  size?: 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  leadingIcon?: React.ReactNode;
  trailingIcon?: React.ReactNode;
  /** Stretch to the container width. Default true. */
  fullWidth?: boolean;
  accessibilityLabel?: string;
}
export declare function Button(props: ButtonProps): JSX.Element;

export interface StatusChipProps {
  status: 'reserving' | 'deploying' | 'ready' | 'failed';
  /** Replaces the default label (Reserving address / Deploying / Ready / Failed). */
  label?: string;
}
export declare function StatusChip(props: StatusChipProps): JSX.Element;

export interface AvatarProps {
  /** Image URL. When absent the initials fallback renders. */
  source?: string | null;
  /** Display name — initials are derived from its first two words. */
  name?: string | null;
  /** Self.xyz-bound → accent ✓ badge bottom-right. */
  verified?: boolean;
  /** sm 28 · md 40 · lg 64 · xl 96. Default md. */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  initials?: string;
  /** Chain id → Base chain badge bottom-left (8453 mainnet, else Sepolia). */
  chainId?: number;
}
export declare function Avatar(props: AvatarProps): JSX.Element;

export interface ChainLogoProps {
  /** 8453 → Base Mainnet; anything else → Base Sepolia. */
  chainId: number;
  /** Rendered size in px. Default 24. */
  size?: number;
}
export declare function ChainLogo(props: ChainLogoProps): JSX.Element;

export interface BottomChipProps {
  label: string;
  /** Leading Lucide icon. */
  icon?: React.ReactNode;
  onPress?: () => void;
  accessibilityLabel?: string;
}
export declare function BottomChip(props: BottomChipProps): JSX.Element;

export interface GlassSurfaceProps {
  /** Corner radius in px. Default 0. */
  radius?: number;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}
export declare function GlassSurface(props: GlassSurfaceProps): JSX.Element;

export interface CofferdamMarkProps {
  /** Rendered size in px. Default 32. */
  size?: number;
  /** CSS colour; defaults to currentColor. */
  color?: string;
  className?: string;
}
export declare function CofferdamMark(props: CofferdamMarkProps): JSX.Element;
