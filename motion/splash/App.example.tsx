import React, { useCallback, useEffect, useState } from 'react';
import { View } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';

import { CofferdamSplash } from './CofferdamSplash';

// Keep the native splash up until our animated overlay has drawn its first frame.
SplashScreen.preventAutoHideAsync();

export default function App() {
  const [appReady, setAppReady] = useState(false);
  const [splashVisible, setSplashVisible] = useState(true);

  useEffect(() => {
    (async () => {
      // load fonts, restore the session, warm caches ...
      setAppReady(true);
    })();
  }, []);

  const hideNativeSplash = useCallback(() => {
    SplashScreen.hideAsync();
  }, []);
  const removeSplash = useCallback(() => setSplashVisible(false), []);

  return (
    <View style={{ flex: 1 }}>
      {/* <YourApp /> renders here, underneath the overlay */}
      {splashVisible && <CofferdamSplash ready={appReady} onMounted={hideNativeSplash} onDone={removeSplash} />}
    </View>
  );
}
