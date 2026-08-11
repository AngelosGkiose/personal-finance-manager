import 'package:flutter/material.dart';

import 'screens/auth/auth_gate.dart';


void main() {
  WidgetsFlutterBinding.ensureInitialized();

  runApp(
    const PersonalFinanceApp(),
  );
}


class PersonalFinanceApp
    extends StatelessWidget {

  const PersonalFinanceApp({super.key});


  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Personal Finance Manager',
      debugShowCheckedModeBanner: false,
      home: const AuthGate(),
    );
  }
}