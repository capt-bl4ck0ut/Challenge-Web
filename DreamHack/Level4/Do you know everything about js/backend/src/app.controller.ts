import { Body, Controller, Post } from "@nestjs/common";
import { AppService } from "./app.service";

type Manifest = {
  links?: { rel: string; href: string; hreflang?: string; title?: string }[];
  schedule?: string;
  headers?: Record<string, string>;
  locale?: string;
};

interface DispatchRequest {
  manifest: Manifest;
}

@Controller()
export class AppController {
  constructor(private readonly svc: AppService) {}

  @Post("dispatch")
  dispatch(@Body() body: DispatchRequest) {
    const manifest = body.manifest;
    const res = this.svc.dispatch(manifest);
    return res;
  }
}
