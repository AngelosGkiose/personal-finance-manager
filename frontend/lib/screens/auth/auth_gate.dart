import 'package:flutter/material.dart';

import '../../services/auth_service.dart';
import '../../storage/token_storage.dart';
import '../home/home_screen.dart';
import 'login_screen.dart';


class AuthGate extends StatefulWidget {
  const AuthGate({super.key});

  @override
  State<AuthGate> createState() => _AuthGateState();
}


class _AuthGateState extends State<AuthGate> {
  late Future<bool> _authenticationFuture;


  @override
  void initState() {
    super.initState();

    _authenticationFuture = _checkAuthentication();
  }


  Future<bool> _checkAuthentication() async {
    final token =
        await TokenStorage.getAccessToken();

    if (token == null || token.isEmpty) {
      return false;
    }

    final isValid =
        await AuthService.validateAccessToken(token);

    if (!isValid) {
      await TokenStorage.deleteAccessToken();
    }

    return isValid;
  }


  void _retry() {
    setState(() {
      _authenticationFuture =
          _checkAuthentication();
    });
  }


  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: _authenticationFuture,

      builder: (context, snapshot) {
        if (snapshot.connectionState !=
            ConnectionState.done) {
          return const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          );
        }

        if (snapshot.hasError) {
          return Scaffold(
            body: Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    'Could not verify your session.',
                  ),

                  const SizedBox(height: 16),

                  ElevatedButton(
                    onPressed: _retry,
                    child: const Text('Retry'),
                  ),
                ],
              ),
            ),
          );
        }

        if (snapshot.data == true) {
          return const HomeScreen();
        }

        return const LoginScreen();
      },
    );
  }
}