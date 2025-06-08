import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS, provideHttpClient, withInterceptors, withInterceptorsFromDi } from '@angular/common/http';
import { TokenInterceptor } from './interceptors/token.interceptor';
import { GoogleLoginProvider, SocialAuthServiceConfig} from '@abacritt/angularx-social-login';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideHttpClient(withInterceptorsFromDi()),
    { provide: HTTP_INTERCEPTORS, useClass: TokenInterceptor, multi: true },
    {
      provide: 'SocialAuthServiceConfig',
      useValue: {
        autoLogin: false, providers: [{ id: GoogleLoginProvider.PROVIDER_ID,
          provider: new GoogleLoginProvider('92500515360-q854c10je9ak7o0e9tsl02d6531crjrg.apps.googleusercontent.com',
            { oneTapEnabled: false, prompt: 'select_account', },  ), },],
      } as SocialAuthServiceConfig,
    },
  ]
};
