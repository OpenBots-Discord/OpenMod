import 'dart:io';

import 'package:nyxx/nyxx.dart';
import 'package:nyxx_interactions/interactions.dart';
import 'package:openmod/shared/instances.dart';

Future<void> main() async {
  client = Nyxx(Platform.environment['OPENMOD_TOKEN']!, GatewayIntents.all);

  interactions = Interactions(client);
  interactions.syncOnReady();
}
