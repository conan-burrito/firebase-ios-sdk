from conans import tools, ConanFile, CMake

import os


class Recipe(ConanFile):
    name = 'firebase-ios-sdk'
    version = '7.3.0'
    description = 'Firebase iOS SDK'
    homepage = 'https://github.com/firebase/firebase-ios-sdk'
    license = 'Apache-2.0 License'
    url = 'https://github.com/conan-burrito/firebase-ios-sdk'

    generators = 'cmake', 'cmake_find_package_multi'

    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {
        'with_analytics': [True, False],
        'with_ab_testing': [True, False],
        'with_app_distribution': [True, False],
        'with_auth': [True, False],
        'with_crashlytics': [True, False],
        'with_database': [True, False],
        'with_dynamic_links': [True, False],
        'with_firestore': [True, False],
        'with_functions': [True, False],
        'with_in_app_messaging': [True, False],
        'with_ml_mode_interpreter': [True, False],
        'with_ml_vision': [True, False],
        'with_messaging': [True, False],
        'with_performance': [True, False],
        'with_remote_config': [True, False],
        'with_storage': [True, False],
        'with_mobile_ads_sdk': [True, False],
        'with_google_sign_in': [True, False],
    }
    default_options = {
        'with_analytics': True,
        'with_ab_testing': False,
        'with_app_distribution': False,
        'with_auth': True,
        'with_crashlytics': False,
        'with_database': True,
        'with_dynamic_links': True,
        'with_firestore': False,
        'with_functions': True,
        'with_in_app_messaging': False,
        'with_ml_mode_interpreter': False,
        'with_ml_vision': False,
        'with_messaging': True,
        'with_performance': False,
        'with_remote_config': True,
        'with_storage': True,
        'with_mobile_ads_sdk': False,
        'with_google_sign_in': False,
    }

    no_copy_source = True
    build_policy = 'missing'

    def configure(self):
        if self.settings.os != 'iOS':
            raise Exception('Only iOS arch is supported')

        if not self.options.with_analytics and (
                self.options.with_ab_testing or self.options.with_app_distribution or self.options.with_auth or
                self.options.with_crashlytics or self.options.with_database or self.options.with_dynamic_links or
                self.options.with_firestore or self.options.with_functions or self.options.with_in_app_messaging or
                self.options.with_ml_mode_interpreter or self.options.with_ml_vision or self.options.with_messaging
                or self.options.with_performance or self.options.with_remote_config or self.options.with_storage or
                self.options.with_mobile_ads_sdk):
            raise Exception('Analytics required')

    @property
    def source_subfolder(self):
        return 'src'

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename('Firebase', self.source_subfolder)

    def collect_frameworks(self):
        frameworks = []
        resources = []
        binaries = []

        def add_frameworks(subdir, libs):
            frameworks.extend([(subdir, x) for x in libs])

        def add_binaries(subdir, bins):
            binaries.extend(['{}/{}'.format(subdir, x) for x in bins])

        def add_resources(subdir, res):
            resources.extend([('{}/Resources/'.format(subdir), x) for x in res])

        # Developer note: see into package sources and add each framework in appropriate `src` directory
        # e.g.: with_ab_testing -> look into FirebaseABTesting. It contains a single file: FirebaseABTesting.xcframework
        # Double check with the README.md file
        if self.options.with_ab_testing:
            add_frameworks('FirebaseABTesting', ['FirebaseABTesting.xcframework'])

        if self.options.with_analytics:
            add_frameworks('FirebaseAnalytics', [
                'FirebaseAnalytics.xcframework',
                'FirebaseCore.xcframework',
                'FirebaseCoreDiagnostics.xcframework',
                'FirebaseInstallations.xcframework',
                'GoogleAppMeasurement.xcframework',
                'GoogleDataTransport.xcframework',
                'GoogleUtilities.xcframework',
                'nanopb.xcframework',
                'PromisesObjC.xcframework',
            ])

        if self.options.with_app_distribution:
            add_frameworks('FirebaseAppDistribution', ['FirebaseAppDistribution.xcframework'])

        if self.options.with_auth:
            add_frameworks('FirebaseAuth', [
                'FirebaseAuth.xcframework',
                'GTMSessionFetcher.xcframework',
            ])

        if self.options.with_crashlytics:
            add_frameworks('FirebaseCrashlytics', ['FirebaseCrashlytics.xcframework'])
            add_binaries('FirebaseCrashlytics', ['run', 'upload-symbols'])

        if self.options.with_database:
            add_frameworks('FirebaseDatabase', [
                'FirebaseDatabase.xcframework',
                'leveldb-library.xcframework',
            ])

        if self.options.with_dynamic_links:
            add_frameworks('FirebaseDynamicLinks', ['FirebaseDynamicLinks.xcframework'])

        if self.options.with_firestore:
            add_frameworks('FirebaseFirestore', [
                'abseil.xcframework',
                'BoringSSL-GRPC.xcframework',
                'FirebaseFirestore.xcframework',
                'gRPC-C++.xcframework',
                'gRPC-Core.xcframework',
                'leveldb-library.xcframework',
            ])
            add_resources('FirebaseFirestore', ['gRPCCertificates-Cpp.bundle'])

        if self.options.with_functions:
            add_frameworks('FirebaseFunctions', [
                'GTMSessionFetcher.xcframework',
                'FirebaseFunctions.xcframework',
            ])

        if self.options.with_in_app_messaging:
            add_frameworks('FirebaseInAppMessaging', [
                'FirebaseInAppMessaging.xcframework',
                'FirebaseABTesting.xcframework',
            ])
            add_resources('FirebaseInAppMessaging', ['InAppMessagingDisplayResources.bundle'])

        if self.options.with_ml_mode_interpreter:
            add_frameworks('FirebaseMLModelInterpreter', [
                'FirebaseMLCommon.framework',
                'FirebaseMLModelInterpreter.framework',
                'GoogleToolboxForMac.xcframework',
                'GTMSessionFetcher.xcframework',
                'Protobuf.xcframework',
                'TensorFlowLiteC.framework',
                'TensorFlowLiteObjC.xcframework',
            ])

        if self.options.with_ml_vision:
            add_frameworks('FirebaseMLVision', [
                'Protobuf.xcframework',
                'FirebaseMLCommon.framework',
                'FirebaseMLVision.framework',
                'GoogleAPIClientForREST.xcframework',
                'GoogleToolboxForMac.xcframework',
                'GTMSessionFetcher.xcframework',
            ])

        if self.options.with_messaging:
            add_frameworks('FirebaseMessaging', [
                'FirebaseInstanceID.xcframework',
                'FirebaseMessaging.xcframework',
            ])

        if self.options.with_performance:
            add_frameworks('FirebasePerformance', [
                'FirebaseABTesting.xcframework',
                'FirebasePerformance.xcframework',
                'FirebaseRemoteConfig.xcframework',
                'GoogleToolboxForMac.xcframework',
                'GTMSessionFetcher.xcframework',
                'Protobuf.xcframework',
            ])

        if self.options.with_remote_config:
            add_frameworks('FirebaseRemoteConfig', [
                'FirebaseABTesting.xcframework',
                'FirebaseRemoteConfig.xcframework',
            ])

        if self.options.with_storage:
            add_frameworks('FirebaseStorage', [
                'FirebaseStorage.xcframework',
                'GTMSessionFetcher.xcframework',
            ])

        if self.options.with_mobile_ads_sdk:
            add_frameworks('Google-Mobile-Ads-SDK', [
                'GoogleMobileAds.xcframework',
                'UserMessagingPlatform.xcframework',
            ])

        if self.options.with_google_sign_in:
            add_frameworks('GoogleSignIn', [
                'AppAuth.xcframework',
                'GoogleSignIn.framework',
                'GTMAppAuth.xcframework',
                'GTMSessionFetcher.xcframework',
            ])
            add_resources('GoogleSignIn', ['GoogleSignIn.bundle', 'GoogleSignIn.bundle.bundle'])

        return frameworks, binaries, resources

    def package(self):
        self.copy('Firebase.h', dst='include', src=self.source_subfolder, keep_path=False)
        self.copy("NOTICES", dst="licenses", src=self.source_subfolder)

        arch = {
            'armv8': 'ios-arm64_armv7',
            'armv7': 'ios-arm64_armv7',
            'x86':    'ios-arm64_i386_x86_64-simulator',
            'x86_64': 'ios-arm64_i386_x86_64-simulator'
        }.get(str(self.settings.arch))

        frameworks, binaries, resources = self.collect_frameworks()
        for x in frameworks:
            name = x[1]
            src_dir = os.path.join(self.source_subfolder, x[0])
            if name.endswith('.xcframework'):
                src_dir = os.path.join(src_dir, name, arch)
                name = name.replace('.xc', '.')
            self.copy('{}/*'.format(name), dst='Frameworks', src=src_dir, symlinks=True)

        for x in binaries:
            self.copy(x, dst='bin', src=self.source_subfolder, keep_path=False)

        for x in resources:
            name = x[1]
            src_dir = os.path.join(self.source_subfolder, x[0])
            self.copy('{}/*'.format(name), dst='res', src=src_dir, symlinks=True)

    def package_id(self):
        # Merge armv7 + armv8 and x86 + x64 architectures
        if self.settings.arch in ['armv7', 'armv8']:
            self.info.settings.arch = 'ARM'

        if self.settings.arch in ['x86', 'x86_64']:
            self.info.settings.arch = 'Simulator'

    def package_info(self):
        frameworks, _, _ = self.collect_frameworks()
        self.cpp_info.frameworks.extend([os.path.splitext(x[1])[0] for x in frameworks])
