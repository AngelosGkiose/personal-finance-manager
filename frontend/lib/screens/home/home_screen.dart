import 'package:flutter/material.dart';

import '../../storage/token_storage.dart';
import '../auth/login_screen.dart';


class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}


class _HomeScreenState extends State<HomeScreen> {
  bool _isLoggingOut = false;


  Future<void> _logout() async {
    setState(() {
      _isLoggingOut = true;
    });

    try {
      await TokenStorage.deleteAccessToken();

      if (!mounted) {
        return;
      }

      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(
          builder: (context) => const LoginScreen(),
        ),
        (route) => false,
      );
    } catch (error) {
      if (!mounted) {
        return;
      }

      setState(() {
        _isLoggingOut = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Could not log out'),
        ),
      );
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Personal Finance Manager',
        ),

        actions: [
          TextButton(
            onPressed: _isLoggingOut ? null : _logout,
            child: _isLoggingOut
                ? const CircularProgressIndicator()
                : const Text('Logout'),
          ),
        ],
      ),

      body: const Center(
        child: Text(
          'You are logged in',
        ),
      ),
    );
  }
}